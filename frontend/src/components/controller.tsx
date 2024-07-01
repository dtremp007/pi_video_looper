import {
  IconPlayerPlay,
  IconPlayerSkipBack,
  IconPlayerSkipForward,
} from "@tabler/icons-solidjs";
import { JSX } from "solid-js/jsx-runtime";
import { cn } from "~/lib/utils";
import * as api from "~/lib/api";

export function VideoController() {
  return (
    <div class="flex gap-4">
      <ControllerButton>
        <IconPlayerSkipBack />
      </ControllerButton>
      <ControllerButton>
        <IconPlayerPlay />
      </ControllerButton>
      <ControllerButton onClick={async () => {
        const result = await api.next();
        console.log(result);
      }}>
        <IconPlayerSkipForward />
      </ControllerButton>
    </div>
  );
}

type ButtonProps = {
  children: JSX.Element;
  class?: string;
} & JSX.IntrinsicElements["button"];

function ControllerButton(props: ButtonProps) {
  return (
    <button
      {...props}
      class={cn("rounded-full bg-muted p-6 active:translate-y-px", props.class)}
    />
  );
}
