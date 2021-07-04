import re
from string import Formatter

from src.globals import *

class NumericEnum(Enum):
	def __init__(self, names):
		d = {name: i for i, name in enumerate(names)}
		super(NumericEnum, self).__init__(d)

class CustomFormatter(Formatter):
	def convert_field(self, value, conversion):
		if conversion == "x": # escape
			return escape_html(value)
		elif conversion == "t": # date[t]ime
			return format_datetime(value)
		elif conversion == "d": # time[d]elta
			return format_timedelta(value)
		return super(CustomFormatter, self).convert_field(value, conversion)

# definition of reply class and types

class Reply():
	def __init__(self, type, **kwargs):
		self.type = type
		self.kwargs = kwargs

types = NumericEnum([
	"CUSTOM",
	"SUCCESS",
	"BOOLEAN_CONFIG",

	"CHAT_JOIN",
	"CHAT_LEAVE",
	"USER_IN_CHAT",
	"USER_NOT_IN_CHAT",
	"GIVEN_COOLDOWN",
	"MESSAGE_DELETED",
	"PROMOTED_MOD",
	"PROMOTED_ADMIN",
	"KARMA_THANK_YOU",
	"KARMA_NOTIFICATION",
	"TRIPCODE_INFO",
	"TRIPCODE_SET",

	"ERR_COMMAND_DISABLED",
	"ERR_NO_REPLY",
	"ERR_NOT_IN_CACHE",
	"ERR_NO_USER",
	"ERR_NO_USER_BY_ID",
	"ERR_ALREADY_WARNED",
	"ERR_NOT_IN_COOLDOWN",
	"ERR_COOLDOWN",
	"ERR_BLACKLISTED",
	"ERR_ALREADY_UPVOTED",
	"ERR_UPVOTE_OWN_MESSAGE",
	"ERR_SPAMMY",
	"ERR_SPAMMY_SIGN",
	"ERR_INVALID_TRIP_FORMAT",
	"ERR_NO_TRIPCODE",
	"ERR_MEDIA_LIMIT",

	"USER_INFO",
	"USER_INFO_MOD",
	"USERS_INFO",
	"USERS_INFO_EXTENDED",

	"PROGRAM_VERSION",
	"HELP_MODERATOR",
	"HELP_ADMIN",
])

# formatting of these as user-readable text

def em(s):
	# make commands clickable by excluding them from the formatting
	s = re.sub(r'[^a-z0-9_-]/[A-Za-z]+\b', r'</em>\g<0><em>', s)
	return "<em>" + s + "</em>"

def smiley(n):
	if n <= 0: return ":)"
	elif n == 1: return ":|"
	elif n <= 3: return ":/"
	else: return ":("

format_strs = {
	types.CUSTOM: "{text}",
	types.SUCCESS: "☑",
	types.BOOLEAN_CONFIG: lambda enabled, **_:
		"<b>{description!x}</b>: " + (enabled and "enabled" or "disabled"),

	types.CHAT_JOIN: em("Вы присоединились к чату!"),
	types.CHAT_LEAVE: em("Вы вышли из чата!"),
	types.USER_IN_CHAT: em("Вы уже в чате."),
	types.USER_NOT_IN_CHAT: em("Вы еще не в чате. Используйте /start присоединяйтесь!"),
	types.GIVEN_COOLDOWN: lambda deleted, **_:
		em( "Вам передано время восстановления этого сообщения на {duration!d}."+
			(deleted and " (сообщение тоже удалено)" or "") ),
	types.MESSAGE_DELETED:
		em( "Ваше сообщение было удалено. Время восстановления не было "
			"учитывая это время, но воздержитесь от повторной публикации." ),
	types.PROMOTED_MOD: em("Вас повысили до модератора, запустите / modhelp, чтобы получить список команд."),
	types.PROMOTED_ADMIN: em("Вас повысили до администратора, запустите / adminhelp, чтобы получить список команд."),
	types.KARMA_THANK_YOU: em("Вы только что подарили этому пользователю сладкую карму, круто!"),
	types.KARMA_NOTIFICATION:
		em( "Тебе только что подарили сладкую карму! (проверьте /info, чтобы увидеть свою карму)"+
			" или /toggleKarma, чтобы отключить эти уведомления)" ),
	types.TRIPCODE_INFO: lambda tripcode, **_:
		"<b>tripcode</b>: " + ("<code>{tripcode!x}</code>" if tripcode is not None else "unset"),
	types.TRIPCODE_SET: em("Набор кодов отключения. Это будет выглядеть так: ") + "<b>{tripname!x}</b> <code>{tripcode!x}</code>",

	types.ERR_COMMAND_DISABLED: em("Эта команда отключена."),
	types.ERR_NO_REPLY: em("Чтобы использовать эту команду, вам необходимо ответить на сообщение."),
	types.ERR_NOT_IN_CACHE: em("Сообщение не найдено в кеше... (прошло 24 часа или бот был перезапущен)"),
	types.ERR_NO_USER: em("No user found by that name!"),
	types.ERR_NO_USER_BY_ID: em("По этому идентификатору не найдено ни одного пользователя! Обратите внимание, что все идентификаторы меняются каждые 24 часа."),
	types.ERR_COOLDOWN: em("Время восстановления истекает через {until!t}"),
	types.ERR_ALREADY_WARNED: em("Для этого сообщения уже было выдано предупреждение."),
	types.ERR_NOT_IN_COOLDOWN: em("У этого пользователя сейчас нет перезарядки."),
	types.ERR_BLACKLISTED: lambda reason, contact, **_:
		em( "Вы попали в черный список" + (reason and " for {reason!x}" or "") )+
		( em("\ncontact:") + " {contact}" if contact else "" ),
	types.ERR_ALREADY_UPVOTED: em("Вы уже проголосовали за это сообщение."),
	types.ERR_UPVOTE_OWN_MESSAGE: em("Вы не можете проголосовать за собственное сообщение."),
	types.ERR_SPAMMY: em("Ваше сообщение не было отправлено. Не отправляйте сообщения слишком быстро, попробуйте позже."),
	types.ERR_SPAMMY_SIGN: em("Ваше сообщение не было отправлено. Избегайте слишком частого использования /sign, попробуйте еще раз позже."),
	types.ERR_INVALID_TRIP_FORMAT:
		em("Данный код поездки недействителен, формат: ")+
		"<code>name#pass</code>" + em("."),
	types.ERR_NO_TRIPCODE: em("У вас нет набора трипкодов."),
	types.ERR_MEDIA_LIMIT: em("В настоящее время вы не можете отправлять мультимедийные сообщения или пересылать сообщения. Повторите попытку позже."),

	types.USER_INFO: lambda warnings, cooldown, **_:
		"<b>id</b>: {id}, <b>username</b>: {username!x}, <b>rank</b>: {rank_i} ({rank})\n"+
		"<b>karma</b>: {karma}\n"+
		"<b>warnings</b>: {warnings} " + smiley(warnings)+
		( " (одно предупреждение будет удалено {warnExpiry!t})" if warnings > 0 else "" ) + ", "+
		"<b>cooldown</b>: "+
		( cooldown and "да, пока {cooldown!t}" or "нет" ),
	types.USER_INFO_MOD: lambda cooldown, **_:
		"<b>id</b>: {id}, <b>username</b>: anonymous, <b>rank</b>: n/a, "+
		"<b>karma</b>: {karma}\n"+
		"<b>cooldown</b>: "+
		( cooldown and "yes, until {cooldown!t}" or "no" ),
	types.USERS_INFO: "<b>{count}</b> <i>users</i>",
	types.USERS_INFO_EXTENDED:
		"<b>{active}</b> <i>active</i>, {inactive} <i>inactive and</i> "+
		"{blacklisted} <i>blacklisted</i> (<i>total</i>: {total})",

	types.PROGRAM_VERSION: "secretlounge-ng v{version} ~ https://github.com/kvmrnnn/secretlounge-ng/",
	types.HELP_MODERATOR:
		"<i>Модераторы могут использовать следующие команды</i>:\n"+
		"  /modhelp - показать этот текст\n"+
		"  /modsay &lt;message&gt; - отправить официальное сообщение модератору\n"+
		"\n"+
		"<i>Или ответьте на сообщение и используйте</i>:\n"+
		"  /info - получить информацию о пользователе, отправившем это сообщение\n"+
		"  /warn - предупредить пользователя, отправившего это сообщение (cooldown)\n"+
		"  /delete - удалить сообщение и предупредить пользователя\n"
		"  /remove - удалить сообщение без перезарядки / предупреждения",
	types.HELP_ADMIN:
		"<i>Admins can use the following commands</i>:\n"+
		"  /adminhelp - показать этот текст\n"+
		"  /adminsay &lt;message&gt; - отправить официальное сообщение админу\n"+
		"  /motd &lt;message&gt; - установить приветствие (HTML formatted)\n"+
		"  /uncooldown &lt;id | username&gt; - убрать кулдаун с пользователя\n"+
		"  /mod &lt;username&gt; - поднять пользователя в ранг модератора\n"+
		"  /admin &lt;username&gt; - поднять пользователя в ранг админа\n"+
		"\n"+
		"<i>Или ответьте на сообщение и используйте</i>:\n"+
		"  /blacklist [reason] - занести в черный список пользователя, отправившего это сообщение",
}

localization = {}

def formatForTelegram(m):
	s = localization.get(m.type)
	if s is None:
		s = format_strs[m.type]
	if type(s).__name__ == "function":
		s = s(**m.kwargs)
	cls = localization.get("_FORMATTER_", CustomFormatter)
	return cls().format(s, **m.kwargs)
