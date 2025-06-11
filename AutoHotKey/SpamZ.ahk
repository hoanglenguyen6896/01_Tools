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
    Loop 20
    {
        Send "Z"
        Sleep 10
    }
}
