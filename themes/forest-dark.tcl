# Copyright (c) 2021 rdbende <rdbende@gmail.com>

# The Forest theme is a beautiful and modern ttk theme inspired by Excel.

package require Tk 8.6

namespace eval ttk::theme::forest-dark {

    variable version 1.0
    package provide ttk::theme::forest-dark $version
    variable colors
    array set colors {
        -fg             "#eeeeee"
        -bg             "#313131"
        -disabledfg     "#595959"
        -disabledbg     "#ffffff"
        -selectfg       "#ffffff"
        -selectbg       "#217346"
    }

    proc LoadImages {imgdir} {
        variable I
        foreach file [glob -directory $imgdir *.png] {
            set img [file tail [file rootname $file]]
            set I($img) [image create photo -file $file -format png]
        }
    }

    LoadImages [file join [file dirname [info script]] forest-dark]

    # Settings
    ttk::style theme create forest-dark -parent default -settings {
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-bg) \
            -focuscolor $colors(-selectbg) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -insertwidth 1 \
            -insertcolor $colors(-fg) \
            -fieldbackground $colors(-selectbg) \
            -font {TkDefaultFont 10} \
            -borderwidth 1 \
            -relief flat

        ttk::style map . -foreground [list disabled $colors(-disabledfg)]

        tk_setPalette background [ttk::style lookup . -background] \
            foreground [ttk::style lookup . -foreground] \
            highlightColor [ttk::style lookup . -focuscolor] \
            selectBackground [ttk::style lookup . -selectbackground] \
            selectForeground [ttk::style lookup . -selectforeground] \
            activeBackground [ttk::style lookup . -selectbackground] \
            activeForeground [ttk::style lookup . -selectforeground]
        
        option add *font [ttk::style lookup . -font]


        # Layouts
        ttk::style layout TButton {
            Button.button -children {
                Button.padding -children {
                    Button.label -side left -expand true
                } 
            }
        }

        ttk::style layout TMenubutton {
            Menubutton.button -children {
                Menubutton.padding -children {
                    Menubutton.indicator -side right
                    Menubutton.label -side right -expand true
                }
            }
        }

        ttk::style layout TOptionMenu {
            OptionMenu.button -children {
                OptionMenu.padding -children {
                    OptionMenu.indicator -side right
                    OptionMenu.label -side right -expand true
                }
            }
        }

        ttk::style layout Accent.TButton {
            AccentButton.button -children {
                AccentButton.padding -children {
                    AccentButton.label -side left -expand true
                } 
            }
        }


        ttk::style layout Switch {
            Switch.button -children {
                Switch.padding -children {
                    Switch.indicator -side left
                    Switch.label -side right -expand true
                }
            }
        }

        ttk::style layout TRadiobutton {
            Radiobutton.button -children {
                Radiobutton.padding -children {
                    Radiobutton.indicator -side left
                    Radiobutton.label -side right -expand true
                }
            }
        }


        ttk::style layout TLabelframe {
            Labelframe.border {
                Labelframe.padding -expand 1 -children {
                    Labelframe.label -side left
                }
            }
        }

        ttk::style layout Treeview.Item {
            Treeitem.padding -sticky nswe -children {
                Treeitem.indicator -side left -sticky {}
                Treeitem.image -side left -sticky {}
                Treeitem.text -side left -sticky {}
            }
        }


        # Elements

        # Button
        ttk::style configure TButton -padding {8 4 8 4} -width -10 -anchor center

        ttk::style element create Button.button image \
            [list $I(rect-basic) \
                {selected disabled} $I(rect-basic) \
                disabled $I(rect-basic) \
                selected $I(rect-basic) \
                pressed $I(rect-basic) \
                active $I(rect-hover) \
            ] -border 4 -sticky nsew

        # Toolbutton
        ttk::style configure Toolbutton -padding {8 4 8 4} -width -10 -anchor center

        ttk::style element create Toolbutton.button image \
            [list $I(empty) \
                {selected disabled} $I(empty) \
                disabled $I(empty) \
                selected $I(rect-basic) \
                pressed $I(rect-basic) \
                active $I(rect-basic) \
            ] -border 4 -sticky nsew

        # Menubutton
        ttk::style configure TMenubutton -padding {8 4 4 4}

        ttk::style element create Menubutton.button image \
            [list $I(rect-basic) \
                disabled $I(rect-basic) \
                pressed $I(rect-basic) \
                active $I(rect-hover) \
            ] -border 4 -sticky nsew 

        ttk::style element create Menubutton.indicator image \
            [list $I(down) \
                active   $I(down) \
                pressed  $I(down) \
                disabled $I(down) \
            ] -width 15 -sticky e

        # OptionMenu
        ttk::style configure TOptionMenu -padding {8 4 4 4}

        ttk::style element create OptionMenu.button image \
            [list $I(rect-basic) \
                disabled $I(rect-basic) \
                pressed $I(rect-basic) \
                active $I(rect-hover) \
            ] -border 4 -sticky nsew 

        ttk::style element create OptionMenu.indicator image \
            [list $I(down) \
                active   $I(down) \
                pressed  $I(down) \
                disabled $I(down) \
            ] -width 15 -sticky e


        # Checkbutton
        ttk::style configure TCheckbutton -padding 4

        ttk::style element create Checkbutton.indicator image \
            [list $I(check-unsel-accent) \
                {alternate disabled} $I(check-tri-basic) \
                {selected disabled} $I(check-basic) \
                disabled $I(check-unsel-basic) \
                {pressed alternate} $I(check-tri-hover) \
                {active alternate} $I(check-tri-hover) \
                alternate $I(check-tri-accent) \
                {pressed selected} $I(check-hover) \
                {active selected} $I(check-hover) \
                selected $I(check-accent) \
                {pressed !selected} $I(check-unsel-pressed) \
                active $I(check-unsel-hover) \
            ] -width 26 -sticky w


        # Sizegrip
        ttk::style element create Sizegrip.sizegrip image $I(sizegrip) \
            -sticky nsew


        # Labelframe
        ttk::style element create Labelframe.border image $I(card) \
            -border 5 -padding 4 -sticky nsew


        # Sashes
        #ttk::style map TPanedwindow -background [list hover $colors(-bg)]
    }
}
