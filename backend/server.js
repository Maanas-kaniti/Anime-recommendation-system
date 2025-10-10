const express = require("express");
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const cors = require("cors");
const Anime = require("./models/Anime");
dotenv.config();

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.log(err));

const app = express();
app.use(cors());
app.use(express.json());

app.get("/anime", async (req, res) => {
  const allanime = await Anime.find().limit(5);
  return res.json(allanime);
});

app.get("/anime/:recomeder", async (req, res) => {
  try {
    const anime = await Anime.find({ rating: req.params.rating }).select(
      "title -_id"
    );

    return res.json(anime);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Server error" });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
