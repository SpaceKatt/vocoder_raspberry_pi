
<CsoundSynthesizer>
<CsOptions>

-odac:hw:2,0 -+rtmidi=portmidi -+rtaudio=alsa -B2048 -b2048 -M0
;-odac:hw:2,0 -+rtmidi=virtual -+rtaudio=alsa -B2048 -b2048 -Ma

</CsOptions>
<CsInstruments>

sr     = 44032
kr     = 256
nchnls = 2
0dbfs  = 1

gisine ftgen 0, 0, 4096, 10, 1

maxalloc 1, 12


;massign 0,     1
;Output  Opcode Arguments    (optional comment)

        instr    1

kbend   linseg 1, 6, .75
kbend   port kbend, 0.001

kpb     pchbend 0, 1600

        iamp = .2
        icps cpsmidi
;output Opcode   amp     freq    fnc         ;comment
a1      oscil    .2,     icps + kpb,   gisine      ;OSC
        outs     a1,a1
        endin


</CsInstruments>
<CsScore>

/*f 0 180; 16 10 1*/

</CsScore>
</CsoundSynthesizer>

