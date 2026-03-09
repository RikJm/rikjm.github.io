import express from "express";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Serve static frontend
app.use(express.static(path.join(__dirname, "..", "public")));

// Get current menu
app.get("/backend/menu", (req, res) => {
  try {
    const data = fs.readFileSync(path.join(__dirname, "menu.json"), "utf8");
    res.json(JSON.parse(data));
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Cannot read menu" });
  }
});

// (Optional) simple protected update endpoint
app.post("/backend/menu", (req, res) => {
  const auth = req.headers["x-admin-key"];
  if (auth !== process.env.ADMIN_KEY) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  try {
    fs.writeFileSync(
      path.join(__dirname, "menu.json"),
      JSON.stringify(req.body, null, 2),
      "utf8"
    );
    res.json({ status: "ok" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Cannot write menu" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
