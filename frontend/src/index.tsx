/* @refresh reload */
import { render } from "solid-js/web";
import "./index.css";
import { Route, Router } from "@solidjs/router";
import Index from "./routes/index";

const root = document.getElementById("root");

render(
  () => (
    <Router>
      <Route path="/" component={Index} />
    </Router>
  ),
  root!
);
