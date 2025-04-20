import "./App.css";
import Layout from "./components/Layout";
import "bootstrap/dist/css/bootstrap.min.css";
import { Routes, Route, BrowserRouter as Router } from "react-router-dom";
import Chat from "./pages/Chat";
import Hoods from "./pages/Hoods";
import New from "./pages/New";
import Profile from "./pages/Profile";
import AllThreads from "./pages/AllThreads";
import MyHoodThreads from "./pages/MyHoodThreads";
import AuthProvider from "./providers/AuthProvider";

function App() {
  return (
    <Router>
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/css/bootstrap.min.css"
        integrity="sha384-SgOJa3DmI69IUzQ2PVdRZhwQ+dy64/BUtbMJw1MZ8t5HZApcHrRKUc4W0kG879m7"
        crossorigin="anonymous"
      />
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/chat" element={<Chat />} />
            <Route path="/hoods" element={<Hoods />} />
            <Route path="/new" element={<New />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/threads/my-hood" element={<MyHoodThreads />} />
            <Route path="/threads/all" element={<AllThreads />} />
          </Routes>
        </Layout>
      </AuthProvider>
    </Router>
  );
}

export default App;
