const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");
const Anime = require("../models/Anime");

router.get("/", async (req, res) => {
  try {
    const title = req.query.title || "";
    const python = spawn("python", ["recommender.py", title]);
    let data = "";
    python.stdout.on("data", (chunk) => {
      data += chunk.toString();
    });
    python.stderr.on("data", (err) => {
      console.error("Python error:", err.toString());
    });

    python.on("close", () => {
      try {
        const result = JSON.parse(data);
        res.json(result);
      } catch (error) {
        console.log(error);
        res.status(500).json({ error: "Invalid response from recommender" });
      }
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
