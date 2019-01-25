# Project: Timer and scrambler for the rubik's cube
# Tekijä: Jere Aho
"""
Kuvaus ohjelmasta:
Ohjelma "CubeTimer.py" mittaa aikaa joka kuuluu käyttäjältä rubiikin kuution selvitykseen ja antaa sekoituksen eri
kokoisille kuutioille.

Satunnaisen sekoituksen eri kuutioille saa painamalla painamalla niiden kuvaketta. Sekoituksen pituus 25 liikettä pitkä.
Lisätietoja kuutioiden liikkeiden notaatiosta löytyy sivuilta: https://ruwix.com/the-rubiks-cube/algorithm/ ja
https://ruwix.com/twisty-puzzles/4x4x4-rubiks-cube-rubiks-revenge/. 3x3 ja 2x2 kuutioiden notaatio on pääosin sama, mutta
4x4 kuutiolla on enemmän liikkeitä.

Ajastin käynnistyy painamalla vihreää "start" nappia ja pysähtyy painamalla "stop" nappia, joka ilmestyi "start" napin
tilalle. Ajastimen voi myös käynnistää ja pysähtyy painamalla välinlyönti nappia. Ajankulu näkyy ”Start/Stop” napin alla.
Selvitys aika otetaan talteen, kun yksi "start" ja "stop" vaihe on käyty läpi. Selvitys aikoja voi halutessaan poistaa
painamalla tallennetun ajan viereen ilmestyvää ruksia tai voidaan myös poistaa kaikki ajat painamalla nappia, jossa lukee
”Clear all the times”. Kaikille selvitys ajoille myös lasketaan keskiarvo, joka päivittyy automaattisesti ajastinta käytettäessä.
"""

from random import *
from tkinter import *
from time import *


CUBES = {"2x2": ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"],
         "3x3": ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"],
         "4x4": ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2",
                 "Rw", "Lw", "Fw", "Bw", "Uw", "Dw", "Rw'", "Lw'", "Fw'", "Bw'", "Uw'", "Dw'", 'Rw2', 'Lw2', 'Fw2',
                 'Bw2', 'Uw2', 'Dw2', "l", "r", "f", "d", "u", "b", "l'", "r'", "f'", "d'", "u'", "b'", 'l2', 'r2',
                 'f2', 'd2', 'u2', 'b2']}
CUBE_AMOUNT = len(CUBES)
CUBEPICS = ["2x2.gif", "3x3.gif", "4x4.gif"]


class GUI:
    def __init__(self):
        self.__window = Tk()
        self.__window.configure(bg="white")
        self.__window.title("Cube Scrambler and Timer")

        """Scrambler part."""
        self.__initial_scramble = True
        self.__scramble = None
        self.__cubes = []
        for cube in CUBES:
            self.__cubes.append(cube)

        self.__cubepics = []
        for pic_file in CUBEPICS:
            pic = PhotoImage(file=pic_file)
            self.__cubepics.append(pic)

        self.__cube_buttons = []
        for i in range(len(CUBES)):
            cubepic = self.__cubepics[i]
            command = lambda j=i: self.set_scramble(j)
            button = Button(self.__window, image=cubepic, command=command)
            button.grid(row=1, column=i)
            self.__cube_buttons.append(button)

        self.__puzzle = Label(text="Choose a puzzle to generate a scramble!",
                              bg="white",
                              borderwidth=2,
                              relief="groove")
        self.__puzzle.grid(row=0, column=1)

        """Cube timer part."""
        self.__elapsed_time = 0
        self.__staring_time = 0
        self.__update = None
        self.__time_widgets = []
        self.__i = 0
        self.__average = 0
        self.__time_label = None
        self.__remove_time = None

        self.__elapsed_time_label = Label(self.__window, text="0.00")
        self.__stop_watch = Button(self.__window, text="Start!",
                                   bg="green",
                                   command=self.start_timer)
        self.__average_label = Label(self.__window, text="Average: 0.00")
        self.__clear_times = Button(self.__window, text="Clear all \n the times",
                                    command=self.clear_times,
                                    state=DISABLED)

        self.__remove_time_image = PhotoImage(file="x.gif")

        self.__row = 4
        self.__elapsed_time_label.grid(row=self.__row + 1, column=0)
        self.__stop_watch.grid(row=self.__row, column=0)
        self.__average_label.grid(row=self.__row - 1, column=1, sticky=E)
        self.__clear_times.grid(row=self.__row + 2, column=0)

        self.__window.bind("<space>", self.start_timer)
        self.__window.grid()

    def start_timer(self, event=None):
        self.__window.bind("<space>", self.stop_timer)
        self.__window.grid()
        self.__staring_time = time()
        self.update_timer()
        self.__stop_watch.configure(text="Stop!",
                                    bg="red",
                                    command=self.stop_timer)

    def stop_timer(self, event=None):
        """ Stops the stopwatch timer."""
        self.__window.bind("<space>", self.start_timer)
        self.__window.grid()
        self.__update = self.__window.after_cancel(self.__update)
        self.add_time()
        self.__staring_time = 0
        self.__stop_watch.configure(text="Start!",
                                    bg="green",
                                    command=self.start_timer)

    def update_timer(self):
        """ Updates the running timer."""
        self.__elapsed_time = time() - self.__staring_time
        self.__elapsed_time_label.configure(text="{:.2f}".format(self.__elapsed_time))
        self.__update = self.__window.after(1, self.update_timer)

    def add_time(self):
        """Adds measured time to saved times."""
        self.__time_label = Label(self.__window, text="{:.2f}".format(self.__elapsed_time))
        self.__remove_time = Button(self.__window, image=self.__remove_time_image,
                                    command=lambda i=self.__i: self.remove_time(i))
        self.__time_label.grid(row=self.__row, column=1, sticky=E)
        self.__remove_time.grid(row=self.__row, column=2, sticky=W)
        self.__row += 1
        self.__i += 1
        self.__time_widgets.append([self.__time_label, self.__remove_time])
        self.__clear_times.configure(state=NORMAL)
        self.calculate_average()

    def calculate_average(self):
        """Calculates the average of the saved times."""
        times = 0
        if len(self.__time_widgets) > 0:
            for time_widget in self.__time_widgets:
                time = time_widget[0]["text"]
                times += float(time)
            average = times / len(self.__time_widgets)
        else:
            average = 0
        self.__average_label.configure(text="Average: {:.2f}".format(average))

    def remove_time(self, i):
        self.__time_widgets[i][0].destroy()
        self.__time_widgets[i][1].destroy()
        del self.__time_widgets[i]
        self.update_times()

    def update_times(self):
        """Updating time widgets. When one saved time is removed, this function will be used."""
        self.__i = 0
        self.__row = 4
        temp_list = []
        for time_widget in self.__time_widgets:
            self.__time_label = time_widget[0]
            self.__remove_time = Button(image=self.__remove_time_image,
                                        command=lambda i=self.__i: self.remove_time(i))
            time_widget[1].destroy()
            self.__time_label.grid(row=self.__row, column=1, sticky=E)
            self.__remove_time.grid(row=self.__row, column=2, sticky=W)
            temp_list.append([self.__time_label, self.__remove_time])
            self.__row += 1
            self.__i += 1
        self.__time_widgets = temp_list

        if len(self.__time_widgets) > 0:
            self.__clear_times.configure(state=NORMAL)
        else:
            self.__clear_times.configure(state=DISABLED)
        self.calculate_average()

    def clear_times(self):
        """Deletes all the saved times."""
        for widgets in self.__time_widgets:
            widgets[0].destroy()
            widgets[1].destroy()
        self.__time_widgets = []
        self.__row = 4
        self.__i = 0
        self.__clear_times.configure(state=DISABLED)
        self.calculate_average()

    def set_scramble(self, j):
        """Generates scramble for cube."""
        cube = self.__cubes[j]
        i = 0
        scramble = []
        previous_letter = ["", "", ""]
        move_list = CUBES[cube]
        while i < 25:
            i += 1
            move = randint(0, len(move_list) - 1)
            first_letter = previous_letter[0] = str(move_list[move][0]).upper()
            second_letter, third_letter = previous_letter[1], previous_letter[2]
            if first_letter == second_letter or first_letter == third_letter:
                i -= 1
            else:
                scramble.append(move_list[move])
                previous_letter[1], previous_letter[2] = previous_letter[0], previous_letter[1]
        scramble = "  ".join(scramble)

        if self.__initial_scramble:
            self.__scramble = Label(self.__window,
                                    bg="white",
                                    text="Scramble: " + scramble,
                                    borderwidth=2,
                                    relief="ridge")
            self.__scramble.grid(row=2,
                                 column=0,
                                 columnspan=CUBE_AMOUNT)
            self.__initial_scramble = False
        else:
            self.__scramble.configure(text="Scramble: " + scramble)

    def start(self):
        self.__window.mainloop()


def main():
    gui = GUI()
    gui.start()


main()