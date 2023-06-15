begin_calendar = '''
<!doctype html>
<html>
<head>
<title>Plano de Estudos Desmoq</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="">
<meta name="author" content="">
<link rel="stylesheet" href="css/ml-calendar.css">
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">
</head>
<body class="ml-calendar-demo">
<div class="ml-calendar">
<section class="calendar-right">
<div class="calendar">
<section class="calendar-header">
<h2><strong>{}</strong> {}</h2>
</section>
<section class="calendar-row">
<div class="calendar-day day-name">Seg</div>
<div class="calendar-day day-name">Ter</div>
<div class="calendar-day day-name">Qua</div>
<div class="calendar-day day-name">Qui</div>
<div class="calendar-day day-name">Sex</div>
<div class="calendar-day day-name">Sab</div>
<div class="calendar-day day-name">Dom</div>
</section>
'''
end_calendar = '''
</div>
</section>
<div class="clear"></div>
</body>
</html>
'''
calendar_day = '''
<div class="calendar-day active">
<span class="calendar-date">{}</span>
{}
</div>
'''
calendar_day_inactive = '''
<div class="calendar-day inactive">
</div>
'''
calendar_start_week = '''
<section class="calendar-row">
'''
calendar_end_week = '''
</section>
'''
calendar_text = '''
<br/><span class="calendar-text">{}</span><span class="calendar-hours">{}</span>
'''
calendar_weekend = '''
<div class="calendar-day weekend">
<span class="calendar-date">{}</span>
{}
</div>
'''
calendar_weekend_inactive = '''
<div class="calendar-day weekend inactive">
</div>
'''



'''
- Layout final: códigos
- Criar página de glossário
- Setar margens PDF client side
- Setar desktop-mode forceful HTML/CSS
- Cores dinâmicas
- SQLAchemy -> POSTGRES Heroku
'''