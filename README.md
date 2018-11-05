# nv-applet

Quick control of the discrete Nvidia GPU in Optimus laptops.

## Usage

Dependencies:

- bbswitch (in Ubuntu, install `bbswitch-dkms`),
- prime-select (typically part of `nvidia-prime`)
- PyGObject (Ubuntu: `python3-gi`)
- [indicator-applet][]
- [nvctl][]

[indicator-applet]: https://github.com/anowlcalledjosh/indicator-applet
[nvctl]: https://github.com/anowlcalledjosh/nvctl

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

## License

GPLv3+

The icon `cpu-frequency-indicator` is from [Paper Icons][paper], which
is licensed under CC BY-SA-4.0.

The Intel and Nvidia icons are from [NVIDIA Power Indicator][n-p-i],
which is licensed under GPLv3.

[paper]: http://snwh.org/paper/icons
[n-p-i]: https://github.com/andrebrait/nvidia-power-indicator
