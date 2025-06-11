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
;
;
;
;
;
;
;

#Singleinstance

/* PES2021 default */
_UP := "{UP}"
_DOWN := "{DOWN}"
_LEFT := "{LEFT}"
_RIGHT := "{RIGHT}"

_CONFIRM := "{ENTER}"
; _CONFIRM := "X"
_BACK := "{ESC}"
; _BACK := "D"

back_to_advanced() {
    Send "{left Down}"
    Sleep 200
    Send "{left Up}"
    Send "{up Down}"
    Sleep 100
    Send "{up Up}"
    Sleep 50
}

skip_match() {
    SendEvent _CONFIRM ; Open Advance menu
    Sleep 50
    SendEvent _UP ; Move to skip
    Sleep 50
    SendEvent _CONFIRM ; Skip
    Sleep 100
    SendEvent _CONFIRM ; Skip
    Sleep 1000
    SendEvent _CONFIRM ; Skip
    Sleep 1000
    SendEvent _CONFIRM ; Skip
    Sleep 100
    ; Sleep 1000
    ; SendEvent _CONFIRM ; Skip
    ; Sleep 1000
    ; SendEvent _CONFIRM ; Skip
    ; Sleep 1000
}

load_formation(num) {
    ; Advanced
    SendEvent _RIGHT ; Team management
    SendEvent _CONFIRM ; Open TM menu
    Sleep 50
    SendEvent _CONFIRM ; Enter Game Plan
    Sleep 800
    ; Send "{right Down}" ; Hold to most right
    ; Sleep 100
    ; Send "{right Up}"
    SendEvent "z"       ; Check Stamina
    SendEvent _LEFT ; Team management
    SendEvent _LEFT ; Team management
    SendEvent _CONFIRM ; Open Save/Load
    SendEvent _DOWN  ; Select Load
    SendEvent _CONFIRM ; Enter Load
    Sleep 200
    if (num == 2)
        SendEvent _DOWN  ; Select 2
    if (num == 3) {
        SendEvent _DOWN  ; Select 2
        SendEvent _DOWN  ; Select 3
    }
    SendEvent _CONFIRM ; Load
    Sleep 50
    SendEvent _CONFIRM ; Confirm Exit
    SendEvent _BACK   ; Back to Save/Load
    SendEvent _BACK   ; Back to Game Plan option
    SendEvent _BACK   ; Back to main
    Sleep 800
    SendEvent _LEFT   ; Back to Advance
    ; Send "{left Down}"
    ; Sleep 200
    ; Send "{left Up}"
}


R::
{
    back_to_advanced()
}

S::
{
    ; MsgBox 1
    SetKeyDelay 100, 50
    back_to_advanced()
    skip_match()
}

; !+1::
1::
{
    ; MsgBox 2
    SetKeyDelay 100, 30
    back_to_advanced()
    load_formation(1)
    skip_match()
}

; !+2::
2::
{
    ; MsgBox 2
    SetKeyDelay 100, 30
    back_to_advanced()
    load_formation(2)
    skip_match()
}

!1::
{
    ; MsgBox "2_1"
    SetKeyDelay 100, 30
    load_formation(1)
}

!2::
{
    SetKeyDelay 100, 30
    load_formation(2)
}


; !Q::
Q::
{
    SetKeyDelay 100, 50
    ; back_to_advanced()
    ; SendEvent _LEFT ; Choose save
    Send "{right Down}"
    Sleep 200
    Send "{right Up}"
    Send "{Up Down}"
    Sleep 200
    Send "{Up Up}"
    ; Sleep 50
    SendEvent _CONFIRM ; Open Sys menu
    Sleep 50
    SendEvent _CONFIRM ; Open Save
    Sleep 2000
    SendEvent _CONFIRM ; Confirm save
    Sleep 200
    SendEvent _RIGHT ; Choose save
    Sleep 100
    SendEvent _CONFIRM ; Confirm save
    Sleep 2000
    Send "{left Down}"
    Sleep 200
    Send "{left Up}"
}


; !D::
N::
{
    SetKeyDelay 100, 50
    SendEvent _CONFIRM ; Open Advanced
    Sleep 100
    SendEvent _CONFIRM ; Choose Next
    Sleep 300
    SendEvent _RIGHT ; Confirm
    Sleep 100
    SendEvent _CONFIRM ; Confirm
}

Send "{alt down}"
Send "{alt up}"

F3::
{
    Loop 99
    {
        Click
        Sleep 10
    }
}