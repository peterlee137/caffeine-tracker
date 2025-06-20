import sys
import os
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QFont

# UI 파일 불러오기
start_ui = uic.loadUiType("start.ui")[0]
ageq_ui = uic.loadUiType("ageq.ui")[0]
weightq_ui = uic.loadUiType("weightq.ui")[0]
mainpage_ui = uic.loadUiType("mainpage.ui")[0]
foodchoice_ui = uic.loadUiType("foodchoice.ui")[0]
records_ui = uic.loadUiType("records.ui")[0]
aboutcaffeine_ui = uic.loadUiType("aboutcaffeine.ui")[0]
options_ui = uic.loadUiType("options.ui")[0]
coffeetype_ui = uic.loadUiType("coffeetype.ui")[0]
coffeeamount_ui = uic.loadUiType("coffeeamount.ui")[0]
chocolatetype_ui = uic.loadUiType("chocolatetype.ui")[0]
chocolateamount_ui = uic.loadUiType("chocolateamount.ui")[0]
softdrinktype_ui = uic.loadUiType("softdrinktype.ui")[0]
energydrinktype_ui = uic.loadUiType("energydrinktype.ui")[0]
teatype_ui = uic.loadUiType("teatype.ui")[0]
drinkamount_ui = uic.loadUiType("drinkamount.ui")[0]
delete_ui = uic.loadUiType("delete.ui")[0]

caffeine_data = {
 'starbucks': 42.62,
 'mcCoffee': 32.65,
 'dunkin': 38.06,
 'coke': 11.86,
 'sprite': 0.0,
 'drPepper': 12.59,
 'gatorade': 15.01,
 'redbull': 28.14,
 'monster': 37.49,
 'greenTea': 10.54,
 'blackTea': 35.72,
 'hersheys' : 20.0,
 'toblerone' : 12.05,
 'snickers' : 4.56
}

# 카페인 제한량 계산 함수
def calculate_caffeine_limit(age, weight):
    if age >= 19:
        return 5 * weight
    elif 10 <= age <= 12:
        return 85
    elif 13 <= age <= 18:
        return 100
    else:
        return 0

# 기록 저장 함수
def save_caffeine_record(date, caffeine_today, caffeine_limit):
    record = f"{date}, {caffeine_today}/{caffeine_limit}\n"
    if os.path.exists("caffeine_records.txt"):
        with open("caffeine_records.txt", "r+") as f:
            lines = f.readlines()
            if len(lines) > 0 and lines[0].startswith(date):
                lines[0] = record  # 이미 오늘의 기록이 있으면 업데이트
            else:
                lines.insert(0, record)  # 없으면 최신 기록을 맨 위로 추가
            f.seek(0)
            f.writelines(lines)
    else:
        with open("caffeine_records.txt", "w") as f:
            f.write(record)

# 기록 읽기 함수
def load_caffeine_records():
    if os.path.exists("caffeine_records.txt"):
        with open("caffeine_records.txt", "r") as f:
            records = f.readlines()
            if not records:
                return ["No Data"] * 7
            return records[:7]  # 최신 7개 기록 반환
    return ["No Data"] * 7

def reset_files():
    # 파일 내용을 초기화 (파일은 남겨두고 내용만 비우거나 초기화)
    with open("caffeine_records.txt", "w") as f:
        f.write("")  # 파일 내용 초기화
    
    with open("userinfo.txt", "w") as f:
        f.write("")  # 파일 내용 초기화

class StartPage(QMainWindow, start_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.button_start.clicked.connect(self.checkUserInfo)

    def checkUserInfo(self):
        if os.path.exists("userinfo.txt"):
            with open("userinfo.txt", "r") as f:
                data = f.read().strip()
                if data:
                    user_data = dict(line.split('=') for line in data.split('\n') if '=' in line)
                    age = int(user_data.get('age', 0))
                    weight = int(user_data.get('weight', 0))
                    if age and weight:
                        caffeine_limit = calculate_caffeine_limit(age, weight)
                        print(f"Setting caffeine_limit to: {caffeine_limit}")
                        self.stacked_widget.parent().setCaffeineLimit(calculate_caffeine_limit(age, weight))
                        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)
                        return
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().ageqPage)

class AgeqPage(QMainWindow, ageq_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.age = None

        self.button_1012.clicked.connect(lambda: self.setAge(12))
        self.button_1318.clicked.connect(lambda: self.setAge(18))
        self.button_19.clicked.connect(lambda: self.setAge(19))
        self.button_back.clicked.connect(self.goBack)

    def setAge(self, age):
        self.age = age
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().weightqPage)

    def goBack(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().startPage)

class WeightqPage(QMainWindow, weightq_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.button_submit.clicked.connect(self.setWeight)
        self.button_back.clicked.connect(self.goBack)

    def setWeight(self):
        font = QFont("더잠실 2 Light", 16)
        self.text_weight.setFont(font)
        weight = self.text_weight.toPlainText()
        age_page = self.stacked_widget.parent().ageqPage
        age = age_page.age

        if age is not None and weight:
            with open("userinfo.txt", "w") as f:
                f.write(f"age={age}\n")
                f.write(f"weight={weight}\n")
            self.stacked_widget.parent().setCaffeineLimit(calculate_caffeine_limit(age, int(weight)))
            self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)
        else:
            print("Error: Age or weight is missing")

    def goBack(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().ageqPage)

class MainPage(QMainWindow, mainpage_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.caffeine_limit = 0
        self.caffeine_today = 0

        self.button_foods.clicked.connect(self.goToFoodChoicePage)
        self.button_records.clicked.connect(self.goToRecordsPage)
        self.button_about.clicked.connect(self.goToAboutCaffeinePage)
        self.button_options.clicked.connect(self.goToOptionsPage)

        self.label_warning.hide()
        self.loadUserInfo()        # 사용자 정보를 로드
        self.loadTodayCaffeine()   # 오늘의 섭취량을 로드

    def loadUserInfo(self):
        if os.path.exists("userinfo.txt"):
            with open("userinfo.txt", "r") as f:
                data = f.read().strip()
                if data:
                    user_data = dict(line.split('=') for line in data.split('\n') if '=' in line)
                    age = int(user_data.get('age', 0))
                    weight = int(user_data.get('weight', 0))
                    if age and weight:
                        self.setCaffeineLimit(calculate_caffeine_limit(age, weight))

    def loadTodayCaffeine(self):
        today = datetime.now().strftime("%Y/%m/%d")
        if os.path.exists("caffeine_records.txt"):
            with open("caffeine_records.txt", "r") as f:
                records = f.readlines()
                for record in records:
                    date, caffeine_data = record.strip().split(', ')
                    if date == today:
                        caffeine_today, _ = map(int, caffeine_data.split('/'))
                        self.updateCaffeineIntake(caffeine_today)
                        break

    def goToFoodChoicePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().foodChoicePage)

    def goToRecordsPage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().recordsPage)
        self.stacked_widget.parent().recordsPage.updateRecords()

    def goToAboutCaffeinePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().aboutCaffeinePage)

    def goToOptionsPage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().optionsPage)

    def setCaffeineLimit(self, limit):
        self.caffeine_limit = limit
        self.label_total.setText(f"/ {self.caffeine_limit}mg")
        self.updateLabelColor()

    def updateCaffeineIntake(self, caffeine):
        self.caffeine_today = caffeine
        self.label_today.setText(f"{round(self.caffeine_today)}")
        self.updateLabelColor()
        today = datetime.now().strftime("%Y/%m/%d")
        save_caffeine_record(today, round(self.caffeine_today), self.caffeine_limit)

    def updateLabelColor(self):
        print(f"caffeine_today: {self.caffeine_today}, caffeine_limit: {self.caffeine_limit}")
        if self.caffeine_limit == 0:
            self.label_warning.hide()
        elif self.caffeine_today > self.caffeine_limit:
            self.label_today.setStyleSheet("color: red;")
            self.label_warning.show()
        else:
            self.label_today.setStyleSheet("color: limegreen;")
            self.label_warning.hide()

class FoodChoicePage(QMainWindow, foodchoice_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.caffeine_limit = 0
        self.caffeine_today = 0

        self.button_back.clicked.connect(self.goToMainPage)
        self.button_coffee.clicked.connect(self.goToCoffeeTypePage)
        self.button_softDrink.clicked.connect(self.goToSoftDrinkTypePage)
        self.button_chocolate.clicked.connect(self.goToChocolateTypePage)
        self.button_energyDrink.clicked.connect(self.goToEnergyDrinkTypePage)
        self.button_tea.clicked.connect(self.goToTeaTypePage)

    def setCaffeineLimit(self, limit):
        self.caffeine_limit = limit
        self.label_total.setText(f"/ {self.caffeine_limit}mg")

    def updateCaffeineIntake(self, caffeine):
        self.caffeine_today = caffeine
        self.label_today.setText(f"{round(self.caffeine_today)}")
        self.updateLabelColor()

    def updateLabelColor(self):
        if self.caffeine_today > self.caffeine_limit:
            self.label_today.setStyleSheet("color: red;")
        else:
            self.label_today.setStyleSheet("color: limegreen;")

    def goToMainPage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)

    def goToCoffeeTypePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().coffeeTypePage)

    def goToSoftDrinkTypePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().softDrinkTypePage)

    def goToChocolateTypePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().chocolateTypePage)

    def goToEnergyDrinkTypePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().energyDrinkTypePage)

    def goToTeaTypePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().teaTypePage)

class RecordsPage(QMainWindow, records_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.caffeine_limit = 0
        self.caffeine_today = 0

        self.button_back.clicked.connect(self.goToMainPage)
        self.setupScrollArea()

    def setupScrollArea(self):
        self.scrollArea.setWidgetResizable(True)
        content_height = 0
        spacing = 15

        records = load_caffeine_records()
        for i in range(1, 8):
            label = getattr(self, f"label_date{i}")
            label.setContentsMargins(0, 15, 0, 0)
            if i <= len(records):
                record = records[i - 1].strip()
                if ', ' in record:
                    dateT, caffeineT = record.split(', ')
                    Y, M, D = dateT.split('/')
                    tdc, ttc = caffeineT.split('/')
                    label.setText(f"<p style='line-height: 150%;'>{Y} / {M} / {D}<br>{tdc} / {ttc}mg</p>")
                else:
                    label.setText("<p style='line-height: 150%;'>No Data</p>")
            else:
                label.setText("<p style='line-height: 150%;'>No Data</p>")
            content_height += label.height() + spacing

        self.scrollAreaWidgetContents.setMinimumHeight(content_height)

    def updateRecords(self):
        self.setupScrollArea()

    def setCaffeineLimit(self, limit):
        self.caffeine_limit = limit
        self.label_total.setText(f"/ {self.caffeine_limit}mg")

    def updateCaffeineIntake(self, caffeine):
        self.caffeine_today = caffeine
        self.label_today.setText(f"{round(self.caffeine_today)}")
        self.updateLabelColor()

    def updateLabelColor(self):
        if self.caffeine_today > self.caffeine_limit:
            self.label_today.setStyleSheet("color: red;")
        else:
            self.label_today.setStyleSheet("color: limegreen;")

    def goToMainPage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)

class AboutCaffeinePage(QMainWindow, aboutcaffeine_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.caffeine_limit = 0
        self.caffeine_today = 0

        self.button_back.clicked.connect(self.goToMainPage)

    def setCaffeineLimit(self, limit):
        self.caffeine_limit = limit
        self.label_total.setText(f"/ {self.caffeine_limit}mg")

    def updateCaffeineIntake(self, caffeine):
        self.caffeine_today = caffeine
        self.label_today.setText(f"{round(self.caffeine_today)}")
        self.updateLabelColor()

    def updateLabelColor(self):
        if self.caffeine_today > self.caffeine_limit:
            self.label_today.setStyleSheet("color: red;")
        else:
            self.label_today.setStyleSheet("color: limegreen;")

    def goToMainPage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)

class OptionsPage(QMainWindow, options_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget

        self.button_back.clicked.connect(self.goToMainPage)
        self.button_changeInfo.clicked.connect(self.goToAgeqPage)
        self.button_reset.clicked.connect(self.goToDeletePage)

    def goToMainPage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)

    def goToAgeqPage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().ageqPage)

    def goToDeletePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().deletePage)

class CoffeeTypePage(QMainWindow, coffeetype_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.selected_drink = None

        self.button_back.clicked.connect(self.goToFoodChoicePage)
        self.button_starbucks.clicked.connect(lambda: self.goToDrinkAmountPage("starbucks"))
        self.button_mcCoffee.clicked.connect(lambda: self.goToDrinkAmountPage("mcCoffee"))
        self.button_dunkin.clicked.connect(lambda: self.goToDrinkAmountPage("dunkin"))

    def goToFoodChoicePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().foodChoicePage)

    def goToDrinkAmountPage(self, drink_type):
        self.selected_drink = drink_type
        drink_amount_page = self.stacked_widget.parent().drinkAmountPage
        drink_amount_page.setPreviousPage(self.stacked_widget.currentWidget())
        drink_amount_page.setDrinkType(drink_type)
        drink_amount_page.clearAmountInput()
        self.stacked_widget.setCurrentWidget(drink_amount_page)

class ChocolateTypePage(QMainWindow, chocolatetype_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.selected_drink = None

        self.button_back.clicked.connect(self.goToFoodChoicePage)
        self.button_hersheys.clicked.connect(lambda: self.goToChocolateAmountPage("hersheys"))
        self.button_toblerone.clicked.connect(lambda: self.goToChocolateAmountPage("toblerone"))
        self.button_snickers.clicked.connect(lambda: self.goToChocolateAmountPage("snickers"))

    def goToFoodChoicePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().foodChoicePage)

    def goToChocolateAmountPage(self, chocolate_type):
        self.selected_drink = chocolate_type
        chocolate_amount_page = self.stacked_widget.parent().chocolateAmountPage
        chocolate_amount_page.setPreviousPage(self.stacked_widget.currentWidget())
        chocolate_amount_page.setChocolateType(chocolate_type)
        chocolate_amount_page.clearAmountInput()
        self.stacked_widget.setCurrentWidget(chocolate_amount_page)

class ChocolateAmountPage(QMainWindow, chocolateamount_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.previous_page = None
        self.current_chocolate_type = None

        self.button_back.clicked.connect(self.goBack)
        self.button_submitG.clicked.connect(self.submitAmount)

    def setPreviousPage(self, previous_page):
        self.previous_page = previous_page

    def setChocolateType(self, chocolate_type):
        self.current_chocolate_type = chocolate_type

    def clearAmountInput(self):
        self.text_g.clear()

    def goBack(self):
        if self.previous_page:
            self.stacked_widget.setCurrentWidget(self.previous_page)

    def submitAmount(self):
        amount_g = self.text_g.toPlainText()
        if amount_g.isdigit() and self.current_chocolate_type in caffeine_data:
            caffeine_per_100g = caffeine_data[self.current_chocolate_type]
            added_caffeine = (int(amount_g) / 100) * caffeine_per_100g
            main_page = self.stacked_widget.parent().mainPage
            new_caffeine_intake = main_page.caffeine_today + added_caffeine
            main_page.updateCaffeineIntake(new_caffeine_intake)

            # 다른 페이지들도 업데이트
            self.stacked_widget.parent().foodChoicePage.updateCaffeineIntake(new_caffeine_intake)
            self.stacked_widget.parent().recordsPage.updateCaffeineIntake(new_caffeine_intake)
            self.stacked_widget.parent().aboutCaffeinePage.updateCaffeineIntake(new_caffeine_intake)

            self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)
        else:
            print("Invalid input or chocolate type")

class SoftDrinkTypePage(QMainWindow, softdrinktype_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.selected_drink = None

        self.button_back.clicked.connect(self.goToFoodChoicePage)
        self.button_coke.clicked.connect(lambda: self.goToDrinkAmountPage("coke"))
        self.button_drPepper.clicked.connect(lambda: self.goToDrinkAmountPage("drPepper"))
        self.button_sprite.clicked.connect(lambda: self.goToDrinkAmountPage("sprite"))

    def goToFoodChoicePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().foodChoicePage)

    def goToDrinkAmountPage(self, drink_type):
        self.selected_drink = drink_type
        drink_amount_page = self.stacked_widget.parent().drinkAmountPage
        drink_amount_page.setPreviousPage(self.stacked_widget.currentWidget())
        drink_amount_page.setDrinkType(drink_type)
        drink_amount_page.clearAmountInput()
        self.stacked_widget.setCurrentWidget(drink_amount_page)

class EnergyDrinkTypePage(QMainWindow, energydrinktype_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.selected_drink = None

        self.button_back.clicked.connect(self.goToFoodChoicePage)
        self.button_gatorade.clicked.connect(lambda: self.goToDrinkAmountPage("gatorade"))
        self.button_redbull.clicked.connect(lambda: self.goToDrinkAmountPage("redbull"))
        self.button_monster.clicked.connect(lambda: self.goToDrinkAmountPage("monster"))

    def goToFoodChoicePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().foodChoicePage)

    def goToDrinkAmountPage(self, drink_type):
        self.selected_drink = drink_type
        drink_amount_page = self.stacked_widget.parent().drinkAmountPage
        drink_amount_page.setPreviousPage(self.stacked_widget.currentWidget())
        drink_amount_page.setDrinkType(drink_type)
        drink_amount_page.clearAmountInput()
        self.stacked_widget.setCurrentWidget(drink_amount_page)

class TeaTypePage(QMainWindow, teatype_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.selected_drink = None

        self.button_back.clicked.connect(self.goToFoodChoicePage)
        self.button_greenTea.clicked.connect(lambda: self.goToDrinkAmountPage("greenTea"))
        self.button_blackTea.clicked.connect(lambda: self.goToDrinkAmountPage("blackTea"))
        self.button_herbalTea.clicked.connect(lambda: self.goToDrinkAmountPage("herbalTea"))

    def goToFoodChoicePage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().foodChoicePage)

    def goToDrinkAmountPage(self, drink_type):
        self.selected_drink = drink_type
        drink_amount_page = self.stacked_widget.parent().drinkAmountPage
        drink_amount_page.setPreviousPage(self.stacked_widget.currentWidget())
        drink_amount_page.setDrinkType(drink_type)
        drink_amount_page.clearAmountInput()
        self.stacked_widget.setCurrentWidget(drink_amount_page)

class DrinkAmountPage(QMainWindow, drinkamount_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.previous_page = None
        self.current_drink_type = None

        self.button_back.clicked.connect(self.goBack)
        self.button_submitMl.clicked.connect(self.submitAmount)

    def setPreviousPage(self, previous_page):
        self.previous_page = previous_page

    def setDrinkType(self, drink_type):
        self.current_drink_type = drink_type

    def clearAmountInput(self):
        self.text_ml.clear()

    def goBack(self):
        if self.previous_page:
            self.stacked_widget.setCurrentWidget(self.previous_page)

    def submitAmount(self):
        amount_ml = self.text_ml.toPlainText()
        if amount_ml.isdigit() and self.current_drink_type in caffeine_data:
            caffeine_per_ml = caffeine_data[self.current_drink_type] / 100.0
            added_caffeine = int(amount_ml) * caffeine_per_ml
            main_page = self.stacked_widget.parent().mainPage
            new_caffeine_intake = main_page.caffeine_today + added_caffeine
            main_page.updateCaffeineIntake(new_caffeine_intake)

            # 다른 페이지들도 업데이트
            self.stacked_widget.parent().foodChoicePage.updateCaffeineIntake(new_caffeine_intake)
            self.stacked_widget.parent().recordsPage.updateCaffeineIntake(new_caffeine_intake)
            self.stacked_widget.parent().aboutCaffeinePage.updateCaffeineIntake(new_caffeine_intake)

            self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)
        else:
            print("Invalid input or drink type")

class DeletePage(QMainWindow, delete_ui):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.button_yes.clicked.connect(self.confirmReset)
        self.button_no.clicked.connect(self.goToMainPage)

    def confirmReset(self):
        reset_files()

        # 시작 페이지로 이동
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().startPage)   

    def goToMainPage(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.parent().mainPage)

class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()

        # 창 크기 고정 설정
        self.setFixedSize(1200, 750)

        # StackedWidget을 사용하여 화면 전환 관리
        self.stackedWidget = QStackedWidget(self)
        self.setCentralWidget(self.stackedWidget)

        # 각 화면 인스턴스 생성 및 StackedWidget에 추가
        self.startPage = StartPage(self.stackedWidget)
        self.ageqPage = AgeqPage(self.stackedWidget)
        self.weightqPage = WeightqPage(self.stackedWidget)
        self.mainPage = MainPage(self.stackedWidget)
        self.foodChoicePage = FoodChoicePage(self.stackedWidget)
        self.recordsPage = RecordsPage(self.stackedWidget)
        self.aboutCaffeinePage = AboutCaffeinePage(self.stackedWidget)
        self.optionsPage = OptionsPage(self.stackedWidget)
        self.coffeeTypePage = CoffeeTypePage(self.stackedWidget)
        self.chocolateTypePage = ChocolateTypePage(self.stackedWidget)
        self.softDrinkTypePage = SoftDrinkTypePage(self.stackedWidget)
        self.energyDrinkTypePage = EnergyDrinkTypePage(self.stackedWidget)
        self.teaTypePage = TeaTypePage(self.stackedWidget)
        self.drinkAmountPage = DrinkAmountPage(self.stackedWidget)
        self.deletePage = DeletePage(self.stackedWidget)
        self.chocolateAmountPage = ChocolateAmountPage(self.stackedWidget)

        self.stackedWidget.addWidget(self.startPage)
        self.stackedWidget.addWidget(self.ageqPage)
        self.stackedWidget.addWidget(self.weightqPage)
        self.stackedWidget.addWidget(self.mainPage)
        self.stackedWidget.addWidget(self.foodChoicePage)
        self.stackedWidget.addWidget(self.recordsPage)
        self.stackedWidget.addWidget(self.aboutCaffeinePage)
        self.stackedWidget.addWidget(self.optionsPage)
        self.stackedWidget.addWidget(self.coffeeTypePage)
        self.stackedWidget.addWidget(self.chocolateTypePage)
        self.stackedWidget.addWidget(self.softDrinkTypePage)
        self.stackedWidget.addWidget(self.energyDrinkTypePage)
        self.stackedWidget.addWidget(self.teaTypePage)
        self.stackedWidget.addWidget(self.drinkAmountPage)
        self.stackedWidget.addWidget(self.deletePage)
        self.stackedWidget.addWidget(self.chocolateAmountPage)

        # 시작 페이지로 이동
        self.stackedWidget.setCurrentWidget(self.startPage)

    def setCaffeineLimit(self, limit):
        self.mainPage.setCaffeineLimit(limit)
        self.foodChoicePage.setCaffeineLimit(limit)
        self.recordsPage.setCaffeineLimit(limit)
        self.aboutCaffeinePage.setCaffeineLimit(limit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())