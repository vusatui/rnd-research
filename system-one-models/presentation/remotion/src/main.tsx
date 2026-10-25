import React from "react";
import { createRoot } from "react-dom/client";
import { Presenter } from "./presenter/Presenter";
import "./presenter/presenter.css";

createRoot(document.getElementById("root")!).render(<Presenter />);
