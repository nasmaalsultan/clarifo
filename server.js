const express = require("express");
const fs = require("fs");
const path = require("path");
const bodyParser = require("body-parser");

const app = express();
const PORT = 3000;

// Serve static files from public folder
app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.json());

// Handle form submission
app.post("/signup", (req, res) => {
  const email = req.body.email;

  if (!email) {
    return res.status(400).send("Email is required");
  }

  fs.appendFile("waitlist.txt", email + "\n", (err) => {
    if (err) {
      console.error("Error saving email:", err);
      return res.status(500).send("Server error");
    }

    res.status(200).send("Email saved");
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server on http://localhost:${PORT}`);
});
