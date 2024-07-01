import { Match, Show, Switch, createEffect, createSignal } from "solid-js";
import * as api from "~/lib/api";
import { Button } from "./ui/button";

export function Updater() {
  const [loading, setLoading] = createSignal(false);
  const [status, setStatus] = createSignal("");

  async function handleUpdate() {
    try {
      const res = await api.updateApplication();
      setLoading(true);
      setStatus(res.status);
    } catch (e) {
      setStatus("Failed to update application");
      setLoading(false);
      return;
    }
    // Await one minute and do a health check
    setTimeout(async () => {
      const health = await api.healthCheck();
      setStatus(health.status);
      setLoading(false);
    }, 60000);
  }

  // Reset error after 5 seconds
  createEffect(() => {
    if (status()) {
      setTimeout(() => {
        setStatus("");
      }, 5000);
    }
  });

  return (
    <>
      <Button onClick={handleUpdate} disabled={loading()}>
        <Switch>
          <Match when={loading()}>Loading...</Match>
          <Match when={true}>Update</Match>
        </Switch>
      </Button>
      <Show when={status()}>
        <p class="text-red-500 text-right">{status()}</p>
      </Show>
    </>
  );
}
