- Nothing receives what the watch sends. `:core-sync` registers no
  `MessageClient.OnMessageReceivedListener` anywhere, so a race sent on
  `/recorded-race` reaches the phone's Data Layer and nothing reads it.
  The phone needs a `WearableListenerService` in `:app-phone`, taking
  its dependencies by injection, that decodes the payload on that path
  and saves the race through `RaceRepository.saveRecordedRace`.

- Nothing receives what the phone sends. Same gap on the other side: a
  profile and reference pushed on `/profile-sync` reach the watch and
  nothing reads them. The watch needs a `WearableListenerService` in
  `:app-wear` that decodes the payload on that path and applies it —
  the profile, the full reference race, and the summarised history,
  replacing the watch's state as a whole.

- `PayloadCodec` encodes and never decodes. It turns a payload into
  bytes for sending and has no path back: nothing turns received bytes
  into a profile, a reference race, a summarised history or a recorded
  race. Both listeners need it.

- The watch erases a race as soon as its send returns true. A
  successful send means the message left the device, not that the phone
  wrote the race down. The watch marks the race as sent and keeps it;
  the phone acknowledges on a third path, `/recorded-race-ack`,
  carrying the race's identifier once it is saved; the watch erases
  only then. A race the phone already holds is acknowledged again and
  not saved twice — the identifier is enough to tell.

- A race sent but not yet acknowledged has no state today.
  `RaceRecordingRepository` stores a recorded race and nothing else:
  after a restart, a sent-but-unacknowledged race is indistinguishable
  from one never sent, and gets sent again. The race carries that
  state, and `observeRecorded` still returns it — it stays in the
  watch's own history until the acknowledgement erases it.
