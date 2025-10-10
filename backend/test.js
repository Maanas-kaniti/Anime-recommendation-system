require("dotenv").config();
const mongoose = require("mongoose");
const Anime = require("./models/Anime"); // your Anime model

mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

mongoose.connection.once("open", async () => {
  console.log("Connected to MongoDB Atlas!");
  const sample = await Anime.find().limit(5);
  console.log(sample);
  mongoose.connection.close();
});
