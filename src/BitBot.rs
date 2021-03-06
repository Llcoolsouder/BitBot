// Program used to analyze market data

extern crate diesel;	//SQLite interface
extern crate time;

struct Coin_data {
	datetime: time::Tm,
	rank: u8,
	price_usd: f64,
	price_btc:f64,
    day_volume_usd: f64,
	market_cap_usd: f64,
	available_supply: f64,
    total_supply: f64,
	percent_change_1h: f32,
	percent_change_24h: f32,
	percent_change_7d: f32,
}

type Coin = Vec<Coin_data>;
/*
fn GetRanks (db: String, table: String) -> Vec<u8> {
	let conn = rusqlite::Connection::open_in_memory().unwrap();
	let mut stmt = conn.prepare(format!("SELECT rank FROM {}", table));
}

fn GetData(db: String, table: String) -> Coin {
	let conn = rusqlite::Connection::open_in_memory().unwrap();
	conn.execute("SELECT rank FROM {};", table)
}
*/

fn main() {
	
}