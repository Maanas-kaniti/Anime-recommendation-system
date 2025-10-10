const mongoose = require("mongoose");
const animeschema = new mongoose.Schema({
  title: String,
  alt_title: String,
  type: String,
  year: String,
  rating: String,
  genres: [String],
  source: String,
  description: String,
  img_url: String,
  page: Number,
  type_only: String,
  episodes: String,
});
const Anime = mongoose.model("Anime", animeschema);

module.exports = Anime;
