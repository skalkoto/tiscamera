# tcam-uvc-extension-loader {#tcam-uvc-extension-loader}

The tcam-uvc-extension-loader is our internal replacement for uvcdynctrl.

It's only purpose is to load UVC extension units for usb cameras.

The description files for the extension units are written in json and are a
direct representation of the underlying struct that is submitted to the kernel.

For a description of the uvc driver mapping command, please refer to the [kernel
documentation](https://www.kernel.org/doc/html/latest/media/v4l-drivers/uvcvideo.html#uvcioc-ctrl-map-map-a-uvc-control-to-a-v4l2-control).

## Arguments

tcam-uvc-extension-loader has the following arguments:

    -h, --help    Show help message and exit
    -d, --device  Device that shall receive the extension unit. (Default: /dev/video0)
    -f, --file    Extension unit file that shall be loaded (This flag is required)

## Exit status

The following return states are possible:

    0   - Normal operation, everthing went ok.
    1   - Device was not found.
    3   - File for extension unit could not be loaded.
    106 - A required argument is missing.

## Extension Unit

The following is a description of the json format that files must adhere to to
be loadable be tcam-uvc-extension-loader.

    {
        # execute `lsusb -vd vid:pid`
        # and search for `guidExtensionCode`
        # the guid from that field has to be entered here
        "guid": "0aba49de-5c0b-49d5-8f71-0be40f94a67a",

        # the list of mappings
        "mappings": [
            {
                # string containing the u32 id number that v4l2
                # will give you when querying the device
                "id": "0x199e9999",
                # String containing the name. Maximum of 31 characters
                "name", "My property",
                # uvc control selector
                "selector": "0xB1",
                # type the uvc property has.
                # possible values are: unsigned, signed, raw, enum, booean, bitmask
                "uvc_type": "",
                # type the v4l2 property has.
                # possible values are: bitmask, boolean, button, integer, menu, string
                v4l2_type: "",
                # size of the uvc property in bit
                size_bits: 8,
                # size of the offset in bit.
                # It is possible to map multiple v4l2 onto the same uvc property field.
                # E.g. this offset allows access to single bit in a bitfield.
                offset_bits 0,

                # entries is an optional field.
                # It is a list of menu entries
                # That shall be mapped
                entries: [
                    {
                        # integer value the v4l2 property shall set in uvc upon selection.
                        value: 999,
                        # String for the entry. Maximum of 31 characters
                        "entry": "My Menu Entry"
                    }
                ]
            }
        ]
    }