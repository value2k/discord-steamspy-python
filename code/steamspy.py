'''
	Discord SteamSpy BOT
	@author Maciej "value" Uliszewski <value2k@gmail.com>
	@copyright Maciej "value" Uliszewski <value2k@gmail.com>
	@license MIT
'''

import discord
from discord.ext import commands
import asyncio, json, urllib.request, string, time


api_key = ""
token = ""

client = commands.Bot(command_prefix='!', description="Takie tam fajne")

steam_sale = "22 Czerwiec 2017 [Niepotwierdzone]"


print ("Uruchamianie bota...")
  
@client.event
async def on_ready():
	print("Uruchomiono...")
	
	
@client.command( name="pomoc", description="Wyświetla dostępne komendy" )
async def pomoc():
	await client.say( "`!pomoc` Wyświetla dostępne komendy\n`!steamsale` Wyświetla datę następnej wyprzedaży steam\n`!cena [nazwa gry]` Wyświetla cenę gry w serwisie steam\n`!konto [steam id]` Wyświetla informacje o koncie steam\n`!autor` Wyświetla autora bota" )
	
	
@client.command( name="autor", description="Wyświetla autora bota" )
async def autor():
	await client.say( "Autorem bota jest ``value`` :point_right: :ok_hand: " )
	

@client.command( name="steamsale", description="Wyświetla datę następnej wyprzedaży steam" )
async def steamsale():
	await client.say( "Następna wyprzedaż steam: " + steam_sale )
	

@client.command( name="profil", description="Wyświetla informację o koncie steam" )
async def profil( steamid = "" ):
	if len(steamid) <= 0:
		await client.say( "Żeby wyświetlić informacje o profilu steam użyj `!profil [steam id]`" )
		return

	response = urllib.request.urlopen( "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + api_key + "&steamids=" + steamid )
	data = json.loads( response.read() )
	
	if len(data['response']['players']) < 1:
		await client.say( "Nie odnaleziono takiego profilu" )
		return
	
	username = "``" + str( data['response']['players'][0]['personaname'] ) + "``"
	country = str( data['response']['players'][0]['loccountrycode'] )
	
	await client.say( username + " [" + country + "]\nData rejestracji: " + time.strftime("%D %H:%M", time.localtime(int( data['response']['players'][0]['timecreated'] ))) + "\nOstatnia aktywność: " +  time.strftime("%D %H:%M", time.localtime(int( data['response']['players'][0]['lastlogoff'] ))) )
	
	
@client.command( name="cena", description="Pokazuje cenę danej gry" )
async def cena( *game_string ):
	if 'game_string' not in locals():
		game_name = "NULL69696912"
	else:
		game_name = ""
		for x in game_string:
			game_name = game_name + x

	if game_name == "NULL69696912" or len(game_name) < 1:
		await client.say( "Jeśli chcesz zobaczyć cenę danej gry wpisz ``!cena [nazwa gry]``")
		return
	
	if game_name.lower().replace(" ", "") == "leagueoflegends":
		await client.say( "Rak rak rak rak ( ͡° ͜ʖ ͡°)")
		return
	
	game_name = str( game_name )
	
	msg = await client.say( "Szukam gry..." )
	
	app_id = str( search_by_name( game_name ) )
	
	if app_id == "-69696969696969691":
		await client.edit_message( msg, "Niestety nie znalazłem takiej gry :V" )
		return
	
	response = urllib.request.urlopen( "http://store.steampowered.com/api/appdetails?appids=" + app_id + "&cc=pl" )
	data = json.loads( response.read() )
	
	if str( data[app_id]['success'] ) == "False":
		await client.edit_message( msg, "Niestety nie znalazłem takiej gry :V" )
		return
		
	game_name = remove_non_ascii( data[ app_id ]['data']['name'] )
	game_f2p = data[ app_id ]['data']['is_free']
	game_price = "0"
	game_currency = "EUR"
	game_sale = "0"
	
	if str( game_f2p ) == "False":
		game_price = str( data[ app_id ]['data']['price_overview']['final']/100 )
		game_currency = str( data[ app_id ]['data']['price_overview']['currency'] )
		game_sale = str( data[ app_id ]['data']['price_overview']['discount_percent'])
		
	
	if str( game_f2p ) == "False":
		if game_sale == "0":
			await client.edit_message( msg, game_name + " kosztuje " + game_price + " " + game_currency )
		else:
			for x in client.get_all_emojis():
				if x.name == "gaben":
					reaction = x
			await client.edit_message( msg, game_name + " kosztuje " + game_price + " " + game_currency + " w przecenie -" + game_sale + "% " + str(reaction) )
	else:
		await client.edit_message( msg, game_name + " jest w modelu Free To Play")
		
	
	

def search_by_name( name = "NULL69696921" ):
	if name == "NULL69696912":
		return "-69696969696969691"
		
	url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/"
	response = urllib.request.urlopen( url )
	data = json.loads( response.read() )
	list = data['applist']['apps']
	count = len(list)
	
	name1 = name.lower()
	
	i = 0
	while (i < count):
		name2 =	list[i]['name'].lower()
		name2 = name2.replace(" ", "")
		
		if name1 == name2:
			return list[i]['appid']
		
		i = i + 1
	
	return "-69696969696969691"


def remove_non_ascii( string = "" ):
	string = ''.join([i if ord(i) < 128 else ' ' for i in string])
	string = string.replace( "<sup>" , "" )
	string = string.replace( "</sup>" , "" )
	return string
	
		

client.run( token )