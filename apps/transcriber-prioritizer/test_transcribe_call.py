"""Stdlib-only tests for transcribe_call pure helpers. Run: python3 -m unittest"""
import unittest

import transcribe_call as tc


class SpeakerHint(unittest.TestCase):
    def test_empty_when_none(self):
        self.assertEqual(tc.speaker_hint_block(None), "")
        self.assertEqual(tc.speaker_hint_block(""), "")

    def test_includes_roster(self):
        out = tc.speaker_hint_block("Alice (PM), Bob (eng)")
        self.assertIn("Alice (PM), Bob (eng)", out)


class TranscribePayload(unittest.TestCase):
    def test_carries_audio_and_format(self):
        p = tc.build_transcribe_payload("BASE64", "mp3", "m", None, 100)
        content = p["messages"][0]["content"]
        audio = next(c for c in content if c["type"] == "input_audio")
        self.assertEqual(audio["input_audio"], {"data": "BASE64", "format": "mp3"})
        self.assertEqual(p["model"], "m")
        self.assertEqual(p["max_tokens"], 100)

    def test_roster_reaches_prompt(self):
        p = tc.build_transcribe_payload("X", "mp3", "m", "Carol (client)", 100)
        text = p["messages"][0]["content"][0]["text"]
        self.assertIn("Carol (client)", text)


class NotesPayload(unittest.TestCase):
    def test_transcript_in_user_turn(self):
        p = tc.build_notes_payload("Speaker 1: hi", "m", None, 100)
        self.assertEqual(p["messages"][0]["role"], "system")
        self.assertIn("Speaker 1: hi", p["messages"][1]["content"])

    def test_notes_prompt_demands_divergence_section(self):
        # The whole point: separate settled understanding from multi-party tension.
        p = tc.build_notes_payload("t", "m", None, 100)
        self.assertIn("Alignment vs. Divergence", p["messages"][0]["content"])


class ExtractText(unittest.TestCase):
    def test_pulls_content(self):
        resp = {"choices": [{"message": {"content": "  hello  "}}]}
        self.assertEqual(tc.extract_message_text(resp), "hello")

    def test_raises_on_bad_shape(self):
        with self.assertRaises(ValueError):
            tc.extract_message_text({"error": "nope"})


class ChooseBitrate(unittest.TestCase):
    def test_short_call_gets_top_rung(self):
        # 10 min easily fits at 64k.
        self.assertEqual(tc.choose_bitrate(600), "64k")

    def test_54min_call_lands_on_32k(self):
        # The real kick-off: ~33 kbps ceiling -> 32k rung.
        self.assertEqual(tc.choose_bitrate(3271), "32k")

    def test_descends_as_duration_grows(self):
        # Monotonic: longer audio never picks a higher bitrate.
        seq = [int(tc.choose_bitrate(d).rstrip("k"))
               for d in (600, 1800, 3271, 5400, 9000)]
        self.assertEqual(seq, sorted(seq, reverse=True))

    def test_unknown_duration_is_safe_default(self):
        self.assertEqual(tc.choose_bitrate(0), "64k")

    def test_very_long_floors_and_flags_overflow(self):
        # 3h at the floor rung still overflows -> caller must chunk.
        self.assertEqual(tc.choose_bitrate(10800), "16k")
        self.assertTrue(tc.payload_exceeds_cap(10800, 16))

    def test_54min_at_32k_fits(self):
        self.assertFalse(tc.payload_exceeds_cap(3271, 32))


if __name__ == "__main__":
    unittest.main()
