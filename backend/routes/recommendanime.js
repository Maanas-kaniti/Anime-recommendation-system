const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");
const Anime = require("../models/Anime");

router.get("/", async (req, res) => {
  try {
    const title = req.query.title || "";
    // Spawn Python script from the backend directory with proper working directory
    const python = spawn("python", ["recommender.py", title], {
      cwd: __dirname, // Run from the backend directory where recommender.py is located
    });
    let data = "";
    python.stdout.on("data", (chunk) => {
      data += chunk.toString();
    });
    python.stderr.on("data", (err) => {
      console.error("Python stderr:", err.toString());
    });

    python.on("close", (code) => {
      try {
        if (!data.trim()) {
          return res
            .status(500)
            .json({ error: "No response from recommender" });
        }
        const result = JSON.parse(data);
        res.json(result);
      } catch (error) {
        console.error("JSON parse error:", error.message);
        console.error("Raw data received:", data);
        res.status(500).json({ error: "Invalid response from recommender" });
      }
    });

    python.on("error", (err) => {
      console.error("Failed to spawn Python process:", err);
      res.status(500).json({ error: "Failed to spawn recommender process" });
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
