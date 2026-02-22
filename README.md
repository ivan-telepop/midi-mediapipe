## Pose / hand landmakrs detection >> convert to MIDI >> Play Synths or Ableton Live

> [!NOTE]
> I still working with it when i have time for it.
---
Time to time i experimenting with python coding and interesting technologies. There is a result of my experiments with Open CV , 
Ableton Live, MIDI IN/OUT. 
In a nutshell here is a video camera which streams video toward Python application so then computer vision detects landmarks on my hands or body. 
The landmarks have coordinates on the screen area, finally they are converted to a data that triggers MIDI params.  I have written the code that encodes this data to MIDI signal so then this MIDI signal generates  sound as you may hear.
experimenting with opencv / mediapipe.

[![Превью видео](images/sc-001.png)](images/screen-rec1.mov)

---
## Детекция поз и переобразование координатных точек с тела в MIDI сигнал далее в MIDI IN/OUT port или в Ableton Live 
> [!NOTE]
> В разработке по мере возможности и времени .

Время от времени я пробую разные технологии. Мини пэт проект. Я переобразовал hand landmarks data в MIDI сигнал. 
Далее сигнал к Ableton MIDI Port... На самом деде можно прикрутить к этой программе синтезаторы, драм машины, или что то софтовое, и это звучит! 
Конечно проект требует развития, графического интерфейса, смены или добавления пресетов с алгоритмами работы, но все же на мой взгляд очень интересный проект. 
Ну или прототип проекта. Буду продолжать его по мере возможности!

## YouTube Video On My Channel
-- 

[![Watch the video](https://img.youtube.com/vi/wMKDv2Fauus/0.jpg)](https://www.youtube.com/watch?v=wMKDv2Fauus)

### Техническое описание проекта :

MIDI:

Если вам когда нибудь доводилось играть на клавишах, синтезаторе, или рояле. То скорее всего вы нажимали на клавиши, педали (если есть), делали 
это с разным усилием, и экспрессией. Возможно даже что-то крутили в виде ручек на панели музыкального инструмента. Все эти действия можно записать в MIDI формат. В нем будут записаны все параметры, усилия, ноты, время нажатий и вообще все что вы делали во время игры.

LANDMARKS:

Видеокамера в компьютере снимает картинку перед собой, а программа детектит ваши руки, позу, положение тела. Как видно на изображении, на теле человека есть точки или маркеры (landmarks) которые расставляются этой программой. Каждая точка имеет координаты в текущее время. Двигаетесь вы, меняются параметры маркеров, по мере вашего движения относительно видео камеры. 
Эти параметры переобразуются в сигнал MIDI, и отправляются в синтезатор. Если коротко, танцуйте, двигайтесь и это будет звучать  !  





docs 
#https://mediapipe.readthedocs.io/en/latest/solutions/hands.html