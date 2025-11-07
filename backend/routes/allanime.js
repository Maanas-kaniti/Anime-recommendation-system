const express = require("express");
const router = express.Router();
const Anime = require("../models/Anime");

router.get("/", async (req, res) => {
  try {
    const Animes = await Anime.find();
    res.json(Animes);
  } catch (err) {
    console.err(log);
    res.status(500).json({ error: "server error while fetching all animes." });
  }
});

module.exports = router;
