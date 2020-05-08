# nv-applet

Quick control of the discrete Nvidia GPU in Optimus laptops.

## Usage

Dependencies:

- bbswitch (in Ubuntu, install `bbswitch-dkms`),
- prime-select (typically part of `nvidia-prime`)
- PyGObject (Ubuntu: `python3-gi`)
- [indicator-applet][]
- [nvctl][]

[indicator-applet]: https://github.com/sersorrel/indicator-applet
[nvctl]: https://github.com/sersorrel/nvctl

You will also need to supply the icons yourself; previous versions of
nv-applet have used the icon `cpu-frequency-indicator` from [Paper
Icons][paper] and the icons from `usr/lib/nvidia-power-indicator/icons`
in [NVIDIA Power Indicator][n-p-i] (replace `nvidia-power-indicator`
with `nv-applet` in the filenames). These icons can't be supplied with
newer versions of nv-applet for licensing reasons.

[paper]: http://snwh.org/paper/icons
[n-p-i]: https://github.com/andrebrait/nvidia-power-indicator

Note: if you're using the `python3-gi` package and are installing
nv-applet into a virtualenv, you'll need to use `--system-site-packages`
or similar when creating the virtualenv.

## Bugs

Undoubtedly.

bbswitch uses an old kernel API to turn the GPU on and off, which
doesn't necessarily work reliably or at all on Linux 4.8+; this is not a
bug in nv-applet.

## Contributing

Please do!

## Copyright

Copyright © 2019 Ash Holland. Licensed under the EUPL (1.2 or later).
