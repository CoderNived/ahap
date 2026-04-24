import "dotenv/config";
import express from "express";
import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";

// ── App setup ────────────────────────────────────────────────────────────────
const app = express();
const PORT = process.env.PORT || 3000;

// ── Middleware ────────────────────────────────────────────────────────────────
app.use(helmet());                          // security headers
app.use(cors());                            // cross-origin requests
app.use(morgan("dev"));                     // request logging
app.use(express.json());                    // parse JSON bodies
app.use(express.urlencoded({ extended: true })); // parse URL-encoded bodies

// ── Routes ────────────────────────────────────────────────────────────────────
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", service: "dhanvantri-api" });
});

// ── Start ─────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`dhanvantri-api running on port ${PORT}`);
});