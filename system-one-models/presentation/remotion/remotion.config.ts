// Remotion Studio / CLI config (npm run studio, npm run render).
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// Use a locally installed Chrome if REMOTION_CHROME is set (otherwise Remotion downloads its own headless shell).
if (process.env.REMOTION_CHROME) Config.setBrowserExecutable(process.env.REMOTION_CHROME);
