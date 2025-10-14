const express = require("express");
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const cors = require("cors");
const Anime = require("./models/Anime");
const { spawn } = require("child_process");
dotenv.config();

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.log(err));

const app = express();
app.use(cors());
app.use(express.json());

app.get("/anime", async (req, res) => {
  const allanime = await Anime.find().select("title -_id");
  return res.json(allanime);
});

app.get("/anime/recommender", async (req, res) => {
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
        res.status(500).json({ error: "Invalid response from recommender" });
      }
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Server error" });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
