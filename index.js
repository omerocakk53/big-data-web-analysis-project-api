const express = require("express");
const cors = require("cors")
const app = express();
const dataRouter = require("./src/router/data-router");

// enable cors
app.use(cors());


app.use('/v1', dataRouter);


const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

