#Requires AutoHotkey v2.0

; Work on full screen 2k monitor UI 110%

#Singleinstance
SetControlDelay -1

ACTION_KEY := "x"
USE_TOOL_KEY := "c"

FrameSleep(x)
{
    ;Input: how many frames you want to sleep for.
    ;Example Usage: FrameSleep(1)
    Sleep x * 16.666
}

GameInput(keys*)
{
    ;Sends keys in a way that game engines can understand.
    ;Input: Key(s) that you want to press.
    ;Example Usage: GameInput("a")
    ;To send multiple keys at the same time: GameInput("a","b","c")
    ;To click: GameInput("LButton")

    for index,key in keys
    {
        downtext .= "{" . key . " down}"
        uptext .= "{" . key . " up}"
    }

    Send downtext
    FrameSleep(1)
    Send uptext
}

GameMouseInput(x, y, key)
{

    MouseClick key, x, y,,,'D'
    Sleep 50
    MouseClick key, x, y,,,'U'
}

; Open chest and add all
; Ctrl & e::
; {
;     ; SendEvent ACTION_KEY
;     GameInput("x")
;     Sleep 500
;     GameMouseInput(1950, 500, "left")
; }
CoordMode "pixel", "screen"
CoordMode "mouse", "screen"
Ctrl & R::
{
    strYourAppExeName := "Stardew Valley.exe"

    ; MouseGetPos &xpos, &ypos
    if WinActive("ahk_exe " strYourAppExeName) {
        ; Errorlevel := PixelSearch(&Px, &Py, 1951, 521, 1951, 521, 0xFFFAE4, 1)
        ; a0 := PixelGetColor(1951, 519)
        ; a1 := PixelGetColor(1950, 500)
        ; MsgBox a0 "--" a1
        ; If PixelSearch(&Px, &Py, 1951, 519, 1952, 520, 0xFFFAE4, 1)
        ;     and PixelSearch(&Px, &Py, 1950, 500, 1951, 501, 0xDB1223, 1)
        ; {
        ;     ; MsgBox "A color within 3 shades of variation was found at X" Px " Y" Py
        ;     ;break
            MouseGetPos &xpos, &ypos
            GameMouseInput(1870, 541, "left")
            Sleep 50
            GameMouseInput(1800, 565, "left")
            MouseMove xpos, ypos
        ; }
        ; MouseGetPos &xpos, &ypos
        ; GameMouseInput(1950, 500, "left")
        ; MouseMove xpos, ypos
        ; Sleep 500
        ; GameInput('e')
    }
    else
    {
        GameInput("Ctrl", "r")
    }

}

Ctrl & A::
{
    strYourAppExeName := "Stardew Valley.exe"

    Loop
    {
        ; MouseGetPos &xpos, &ypos
        if WinActive("ahk_exe " strYourAppExeName) {
            MouseGetPos &xpos, &ypos
            GameMouseInput(xpos, ypos, "left")
            Sleep 1000
        }
        else
        {
            GameInput("Ctrl", "a")
            break
        }
    } Until (GetKeyState("Ctrl") || GetKeyState("A"))
}

Q::
{
    strYourAppExeName := "Stardew Valley.exe"
    ; MouseGetPos &xpos, &ypos
    if WinActive("ahk_exe " strYourAppExeName) {
        GameInput("1")
    }
    else
    {
        GameInput("q")
    }
}

; Open chest and add all
; Ctrl & q::
; {
;     ; MouseClick "left", 1950, 500
;     ; Click 1950, 500, "Left"
;     GameMouseInput(1950, 500, "left")
; }
