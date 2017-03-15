# gmail2fritzbox

Convert contacts exported from gmail as .csv to an .xml that can be imported as
phonebook on a FritzBox 6360 Cable.

The Fritzbox has a Gmail Sync function, but because gmail always adds the
country code in front of all phone numbers, there is no way to not have `+49`
(for Germany in my case) at the beginning of every number in the fritzbox
phonebook.

In my case this leads to the connected fritz phones not showing the names of
callers, because the incoming numbers do not have the `+49` prefix and therefore
are not matched to the phone book entries.

This is my workaround.

It uses only the `Name` and the 4 `Phone...` fields from the gmail .csv.
Everything else is discarded. The resulting .xml is not formatted exceptionally
well. The `+49` prefix is not replaced with a `0`, which may look weird, but it
works for my usecase.

Feel free to use and this as you want, but do so at your own risk.

I have not added any error handling (nor do plan to do so) and the output file
is overridden without asking, if it existed previously.
