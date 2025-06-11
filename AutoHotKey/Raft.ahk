#Requires AutoHotkey v2.0
; # = Win
; ! = Alt
; ^ = Ctrl
; + = Shift
; & - Combine some keys together
; < or > = use left or right key of the pair (2 Shift, 2 Ctrl, ...)
; * = wildcard - match anything even empty
; ~ = Block native key function (like Esc is not Esc anymore, ...)
; $
; UP = release key action (work with combination)
;

Alt & e::
{
    Loop 10
    {
        Send "E"
        Sleep 50
    }
}

Alt & c::
{
    Send "E"
    Sleep 100
    Send "C"
    Sleep 100
    Send "E"
}

;if PixelSearch(&Px, &Py, -195, 302, -138, 337, 0x5F3822, 1)
;    MsgBox "A color within 3 shades of variation was found at X" Px " Y" Py
;else
;    MsgBox "That color was not found in the specified region."

^!z::  ; Control+Alt+Z hotkey.
{
    MouseGetPos &MouseX, &MouseY
    MsgBox "The color at the current cursor position is " PixelGetColor(MouseX, MouseY) " " MouseX " " MouseY
}

; Auto fish
Alt & f::
{
    Loop
    {
        ; Middle 1280 720
        Errorlevel := PixelSearch(&Px, &Py, 1250, 595, 1313, 625, 0xE6D4B5, 1)
        If (Errorlevel = 1)
        {
            ;MsgBox "A color within 3 shades of variation was found at X" Px " Y" Py
            ;break
            MouseClick "left"
            Sleep 500
            MouseClick "left"
        }
    } Until (GetKeyState("Ctrl") || GetKeyState("f"))
    ;MsgBox "That color was not found in the specified region."
}

Alt & w::
{
    Loop
    {
        Send "{W Down}"
        Sleep 100
    } Until (GetKeyState("Ctrl") || GetKeyState("s"))
    Send "{W Up}"
}


; Place potato auto
; 1199 1170 5F3822
; 1199 1188
; 1218 1176

; 1201 628 F4E4C2
; 1201 643
; 1212 628
; 1212 643
; 1260 628
; 1260 643

Alt & p::
{
    Loop
    {
        potato0_0 := PixelGetColor(1199, 1170)
        potato0_1 := PixelGetColor(1199, 1188)
        potato0_2 := PixelGetColor(1218, 1176)

        potato1_0 := PixelGetColor(1201, 629)
        potato1_1 := PixelGetColor(1201, 640)
        potato1_2 := PixelGetColor(1212, 629)
        potato1_3 := PixelGetColor(1212, 640)
        potato1_4 := PixelGetColor(1260, 629)
        potato1_5 := PixelGetColor(1260, 640)
        ;MsgBox potato0_0 " " potato0_1 " " potato0_2
        ;MsgBox potato1_0 " " potato1_1 " " potato1_2 " " potato1_3 " " potato1_4 " " potato1_5
        if (potato0_0 = potato0_1
                and potato0_0 = potato0_2
                and potato0_0 = 0x5F3822
                and potato1_0 = potato1_1
                and potato1_0 = potato1_2
                and potato1_0 = potato1_3
                and potato1_0 = potato1_4
                and potato1_0 = potato1_5
                and potato1_0 = 0xF4E4C2)
            Send "E"
            ;Sleep 10

    } Until (GetKeyState("Ctrl") || GetKeyState("p"))
}

/*
Alt & p::
{
    Loop
    {
        ; Middle 1280 720
        Errorlevel := PixelSearch(&Px, &Py, 1190, 1165, 1120, 1195, 0xE6D4B5, 1)
        Errorlevel1 := PixelSearch(&Px, &Py, 1270, 565, 1290, 570, 0xE6D4B5, 1)
        If (Errorlevel = Errorlevel1 and Errorlevel1 = 1)
        {
            potato1_0 := PixelGetColor(1201, 629)
            potato1_1 := PixelGetColor(1201, 640)
            potato1_2 := PixelGetColor(1212, 629)
            potato1_3 := PixelGetColor(1212, 640)
            potato1_4 := PixelGetColor(1260, 629)
            potato1_5 := PixelGetColor(1260, 640)
            ;MsgBox potato0_0 " " potato0_1 " " potato0_2
            ;MsgBox potato1_0 " " potato1_1 " " potato1_2 " " potato1_3 " " potato1_4 " " potato1_5
            if (potato1_0 = potato1_1
                    and potato1_0 = potato1_2
                    and potato1_0 = potato1_3
                    and potato1_0 = potato1_4
                    and potato1_0 = potato1_5
                    and potato1_0 = 0xF4E4C2)
                Send "E"
                ;Sleep 10
        }
    } Until (GetKeyState("Ctrl") || GetKeyState("p"))
    ;MsgBox "That color was not found in the specified region."
}
*/

Alt & h::
{
    Loop
    {
        MouseClick "left", 1245, 430
        Sleep 500
        MouseClick "left", 194, 1236
        Sleep 500
    } Until (GetKeyState("Ctrl") || GetKeyState("f"))
    ;MsgBox "That color was not found in the specified region."
}