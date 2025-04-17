import "./App.css";
import Layout from "./components/Layout";
import "bootstrap/dist/css/bootstrap.min.css";
import { Routes, Route, BrowserRouter as Router } from "react-router-dom";
import Chat from "./pages/Chat";
import Hoods from "./pages/Hoods";
import New from "./pages/New";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/chat" element={<Chat />} />
          <Route path="/hoods" element={<Hoods />} />
          <Route path="/new" element={<New />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
