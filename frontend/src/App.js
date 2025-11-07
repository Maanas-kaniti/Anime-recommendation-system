import React from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [searchTerm, setSearchTerm] = React.useState("");
  const [recommendations, setRecommendations] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      setError("Please enter a valid anime name.");
      return;
    }
    setLoading(true);
    setError(null);
    setRecommendations([]);
    try {
      const response = await axios.get(
        `http://localhost:5000/api/recommend?title=${searchTerm}`
      );
      console.log("API response:", response.data);
      setRecommendations(response.data || []);
    } catch (err) {
      setError("Failed to fetch recommendations. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="app">
      <h1>Anime Recommendation System</h1>
      <div className="search-box">
        <input
          type="text"
          placeholder="enter anime title..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button onClick={handleSearch}>Get Recommendations</button>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      <div className="results">
        {recommendations.length > 0 ? (
          <ul>
            {recommendations.map((anime, index) => (
              <li key={index}>{anime}</li>
            ))}
          </ul>
        ) : (
          !loading && !error && <p>No recommendations to display.</p>
        )}
      </div>
    </div>
  );
}

export default App;
