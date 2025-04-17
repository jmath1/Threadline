import "./App.css";
import Layout from "./components/Layout";
import "bootstrap/dist/css/bootstrap.min.css";
import { Routes, Route, BrowserRouter as Router } from "react-router-dom";
import Chat from "./pages/Chat";
import Hoods from "./pages/Hoods";
import New from "./pages/New";
import Profile from "./pages/Profile";
import AuthProvider from "./providers/AuthProvider";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/chat" element={<Chat />} />
            <Route path="/hoods" element={<Hoods />} />
            <Route path="/new" element={<New />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </Layout>
      </AuthProvider>
    </Router>
  );
}

export default App;
