CREATE OR REPLACE FUNCTION check_user_coords()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the new coordinates are within the geographic boundary of the assigned block
    IF (NEW.coords IS NOT NULL OR NEW.block_id IS NOT NULL) THEN
        IF NOT EXISTS (
            SELECT 1 FROM Block
            WHERE block_id = NEW.block_id
            AND ST_Contains(coords, NEW.coords)
        ) THEN
            RAISE EXCEPTION 'New block/coordinates are outside the designated block boundary.';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION check_message_location()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the message is associated with a specific block or hood and validate accordingly
    IF (NEW.thread_id IS NOT NULL) THEN
        -- Retrieve the block_id and hood_id associated with the thread_id
        DECLARE
            block_id_var INT;
            hood_id_var INT;
        BEGIN
            SELECT block_id, hood_id INTO block_id_var, hood_id_var FROM Thread WHERE thread_id = NEW.thread_id;
            
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Thread with id % not found.', NEW.thread_id;
            END IF;

            IF block_id_var IS NOT NULL THEN
                -- If there is a block_id, check that the message's coords are within this block's radius
                IF NOT EXISTS (
                    SELECT 1
                    FROM Block
                    WHERE Block.block_id = block_id_var
                    AND ST_DWithin(Block.coords::geography, NEW.coords::geography, Block.radius)
                ) THEN
                    RAISE EXCEPTION 'Message coordinates are outside the designated block boundary.';
                END IF;
            ELSIF hood_id_var IS NOT NULL THEN
                -- If there is a hood_id, check that the message's coords are within any block of this hood
                IF NOT EXISTS (
                    SELECT 1
                    FROM Block
                    WHERE Block.hood_id = hood_id_var
                    AND ST_DWithin(Block.coords::geography, NEW.coords::geography, Block.radius)
                ) THEN
                    RAISE EXCEPTION 'Message coordinates are outside any blocks of the specified hood.';
                END IF;
            END IF;
        END;
    ELSE
        RAISE EXCEPTION 'Message must be associated with a thread.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER check_message_location
BEFORE INSERT OR UPDATE OF coords ON Message
FOR EACH ROW
EXECUTE FUNCTION check_message_location();





CREATE OR REPLACE FUNCTION notify_users()
RETURNS TRIGGER AS $$
DECLARE
 block_id_var INT;
 hood_id_var INT;
 notification_type VARCHAR(50);
BEGIN
 -- Fetch block_id and hood_id based on coordinates
 SELECT b.block_id, b.hood_id INTO block_id_var, hood_id_var
 FROM Block b
 WHERE EXISTS (
     SELECT 1
     FROM Message m
     WHERE m.thread_id = NEW.thread_id
     AND ST_DWithin(m.coords::geography, b.coords::geography, b.radius)
 );


 -- Notification type based on block_id or hood_id
 IF block_id_var IS NOT NULL THEN
     notification_type := '1';
 ELSIF hood_id_var IS NOT NULL THEN
     notification_type := '2';
 ELSE
     notification_type := '3'; -- For UserThread
 END IF;


 -- Insert notifications for users in the block, hood, or UserThread
 IF notification_type IN ('1', '2') THEN
     INSERT INTO Notifications (to_user, user_id, notification_type, thread_id, message_id, datetime)
     SELECT DISTINCT p.user_id AS to_user,
                     NEW.user_id,
                     notification_type,
                     NEW.thread_id,
                     NEW.message_id,
                     NOW()
     FROM Profile p
     JOIN Block b ON ST_DWithin(p.coords::geography, b.coords::geography, b.radius)
     WHERE ((b.block_id = block_id_var AND notification_type = '1')
     OR (b.hood_id = hood_id_var AND notification_type = '2')) AND p.user_id != NEW.user_id;
 ELSE
     -- For UserThread
     INSERT INTO Notifications (to_user, user_id, notification_type, thread_id, message_id, datetime)
     SELECT DISTINCT ut.user_id AS to_user,
                     NEW.user_id,
                     notification_type,
                     NEW.thread_id,
                     NEW.message_id,
                     NOW()
     FROM UserThread ut
     WHERE ut.thread_id = NEW.thread_id AND ut.user_id != NEW.user_id;
 END IF;


 RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER notify_users
AFTER INSERT ON Message
FOR EACH ROW
EXECUTE FUNCTION notify_users();



CREATE OR REPLACE FUNCTION notify_friendship_request()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Notifications (to_user, user_id, notification_type, datetime)
    VALUES (NEW.followee_id, NEW.follower_id, 'Friendship Request', NOW());
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER friendship_request_notification
AFTER INSERT ON Friendship
FOR EACH ROW
WHEN (NEW.confirmed = false)  -- Trigger only when a friendship request is made
EXECUTE FUNCTION notify_friendship_request();


CREATE OR REPLACE FUNCTION notify_friendship_confirmation()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Notifications (to_user, user_id, notification_type, datetime)
    VALUES (NEW.followee_id, NEW.follower_id, 'Friendship Confirmation', NOW());
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER friendship_confirmation_notification
AFTER UPDATE ON Friendship
FOR EACH ROW
WHEN (OLD.confirmed = false AND NEW.confirmed = true)  -- Trigger only when a friendship request is confirmed
EXECUTE FUNCTION notify_friendship_confirmation();

-- Create a new friend for user_id 10 in the same hood
INSERT INTO Friendship (follower_id, followee_id, confirmed)
VALUES (10, 20, true);

-- Create a new friend for user_id 10 in a different hood
INSERT INTO Friendship (follower_id, followee_id, status)
VALUES (10, (SELECT user_id FROM Profile WHERE user_id != 10 AND hood_id != (SELECT hood_id FROM Profile WHERE user_id = 10) LIMIT 1), 'requested');

SELECT m.message_id, m.thread_id, m.body, m.user_id, m.datetime AS message_datetime
FROM Message m
JOIN Thread t ON m.thread_id = t.thread_id
JOIN UserThread ut ON t.thread_id=ut.thread_id -- only those that the user is tagged in
WHERE (t.block_id IS NULL AND t.hood_id IS NULL) -- Consider only messages not associated with blocks or hoods
AND m.body LIKE '%bicycle%' AND ut.user_id = 10;