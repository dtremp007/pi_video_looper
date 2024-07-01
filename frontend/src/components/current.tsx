import { Show, createResource } from "solid-js";
import * as api from "~/lib/api";

export function CurrentVideo() {
    const [current] = createResource(api.currentVideo)

    return (
        <Show when={current()}>
                <h2>{current()?.title}</h2>
        </Show>
    )
}
