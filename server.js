const express = require("express");
const { spawn } = require("child_process");
const path = require("path");

const app = express();
const PORT = 3000;

app.use("/tiles", express.static(path.join(__dirname, "tiles")));

app.get("/update/:radar/:product", (req, res) => {
    const { radar, product } = req.params;

    const process = spawn("python3", [
        "radar_engine.py",
        radar,
        product
    ]);

    process.on("close", () => {
        res.json({ status: "updated", radar, product });
    });
});

app.listen(PORT, () => {
    console.log("WeatherWise backend running on port " + PORT);
});