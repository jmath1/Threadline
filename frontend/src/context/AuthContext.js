// import React, { createContext, useContext, useState, useEffect } from 'react';
// import axios from 'axios';

// const AuthContext = createContext(null);

// export const useAuthentication = () => {
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchUser = async () => {
//       try {
//         const response = await axios.get('http://0.0.0.0:8000/user/me/', {
//           withCredentials: true,
//         });
//         if (response.data) {
//           console.log(response.data);
//           setUser(response.data);
//         } else {
//           setUser(null);
//         }
//       } catch (error) {
//         console.error("Error fetching user details:", error);
//         setUser(null);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchUser();
//   }, []);

//   return { user, loading };
// };

// export const AuthProvider = ({ children }) => {
//   return (
//     <AuthContext.Provider value={useAuthentication()} >
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export const useAuth = () => useContext(AuthContext);
