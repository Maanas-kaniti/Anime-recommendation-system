require("dotenv").config();
const mongoose = require("mongoose");
const fs = require("fs");
const csv = require("csv-parser");

mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
console.log("MONGO_URI:", process.env.MONGO_URI); // Add this line after require("dotenv").config();
const animeSchema = new mongoose.Schema({
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

const Anime = mongoose.model("Anime", animeSchema);
const results = [];
fs.createReadStream("../data/anime_planet_full_details_cleaned.csv")
  .pipe(csv())
  .on("data", (row) => results.push(row))
  .on("end", async () => {
    try {
      await Anime.insertMany(results);
      console.log("Data successfully imported to Atlas!");
      mongoose.connection.close();
    } catch (error) {
      console.error("Error inserting data:", error);
      mongoose.connection.close();
    }
  });
