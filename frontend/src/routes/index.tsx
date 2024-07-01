import { VideoController } from "~/components/controller";
import { CurrentVideo } from "~/components/current";
import { Updater } from "~/components/updater";

export default function Index() {
  return (
    <div class="container">
      <h1 class="text-2xl font-bold text-center">Adafruit Video Looper</h1>
      <div class="flex flex-col items-center">
        <Updater />
      </div>
      <div class="flex justify-center items-center h-screen">
        <CurrentVideo />
        <VideoController />
      </div>
    </div>
  );
}
