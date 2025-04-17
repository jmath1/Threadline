import "./App.css";
import Layout from "./components/Layout";
import AuthProvider from "./providers/AuthProvider";
import "bootstrap/dist/css/bootstrap.min.css";
function App() {
  return (
    <AuthProvider>
      <Layout>
        <header className="App-header">
          <p>Starting my Threadline App here</p>
          <a
            className="App-link"
            href="https://jonathanmath.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            jonathanmath.com
          </a>
        </header>
      </Layout>
    </AuthProvider>
  );
}

export default App;
