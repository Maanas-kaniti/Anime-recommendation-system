const express = require("express");
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const cors = require("cors");
const Anime = require("./models/Anime");

const allanimesRoute = require("./routes/allanime");
const recommendRoute = require("./routes/recommendanime");
dotenv.config();

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.log(err));

const app = express();
app.use(cors());
app.use(express.json());

app.use("/api/recommend", recommendRoute);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
