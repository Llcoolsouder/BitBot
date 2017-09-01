extern crate num;
use num::Num;

#[cfg(test)]
mod tests {
use super::*;
    #[test]
    fn it_works() {
    }

	#[test]
	fn mean_test() {
		let tvec: Vec<f32> = vec![1f32, 2f32, 3f32, 4f32, 5f32, 6f32, 7f32, 8f32, 9f32, 10f32];
		let uvec: Vec<f64> = vec![4f64, 8f64, 15f64, 16f64, 23f64, 42f64];
		let vvec: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
		assert_eq!(mean(&tvec), 5.5f64);
		assert_eq!(mean(&uvec), 18f64);
		assert_eq!(mean(&vvec), 5.5f64);
	}


	#[test]
	fn std_dev_test() {
		let tvec: Vec<f32> = vec![1f32, 2f32, 3f32, 4f32, 5f32, 6f32, 7f32, 8f32, 9f32, 10f32];
		let uvec: Vec<f64> = vec![4f64, 8f64, 15f64, 16f64, 23f64, 42f64];
		let vvec: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
		println!("TVec StdDev: {}", std_dev(&tvec));
		println!("UVec StdDev: {}", std_dev(&uvec));
		assert_eq!(std_dev(&tvec), 2.8722813232690143);
		assert_eq!(std_dev(&uvec), 12.315302134607444);
		assert_eq!(std_dev(&vvec), 2.8722813232690143);
	}

	#[test]
	fn sma_test() {
		let tvec: Vec<f32> = vec![1f32, 2f32, 3f32, 4f32, 5f32, 6f32, 7f32, 8f32, 9f32, 10f32];
		let sma: Vec<f64> = simple_moving_average(3, &tvec);
		println!("SMA: {:?}", sma);
	}

	#[test]
	fn bollinger_test() {
		let tvec: Vec<f32> = vec![1f32, 2f32, 3f32, 4f32, 5f32, 6f32, 7f32, 8f32, 9f32, 10f32];
		let b_bands: BollingerBands<f64> = get_bollinger_bands(3usize, 2f64, &tvec);
		println!("{:?}", b_bands);
	}

}

#[derive(Debug)]
pub struct BollingerBands<T: Num> {
	high_band: Vec<T>,
	mid_band: Vec<T>,
	low_band: Vec<T>,
}


///Trait used simply for explicit conversion of numeric types
pub trait Convertible{
	fn tof64(self) -> f64;
}

impl Convertible for i32 {
	fn tof64(self) -> f64{
		self as f64
	}
}

impl Convertible for usize {
	fn tof64(self) -> f64{
		self as f64
	}
}

impl Convertible for f32 {
	fn tof64(self) -> f64{
		self as f64
	}
}

///This function is only implemented because in some cases,
/// the numeric type _could_ be an f64, so this function,
/// while seemingly unnecessary, must be implemented
impl Convertible for f64 {
	fn tof64(self) -> f64{
		self
	}
}


pub fn sum<T: Num + Copy>(v: &Vec<T>) -> T {
	let mut sum = num::zero();
	for i in v {
		sum = sum + *i;
	}
	sum
}

pub fn mean<T: Num + Convertible + Copy >(v: &Vec<T>) -> f64 {
	match v.len() {
		0 => 0f64,
		_ => sum(&v).tof64()/v.len() as f64
	}
}


pub fn std_dev<T: Num + Convertible + Copy>(v: &Vec<T>) -> f64 {
	let x_bar: f64 = mean(&v);
	let mut numerator: f64 = 0f64;
	for x in v {
		numerator = numerator + (x.tof64() - x_bar).abs().powf(2f64);
	}
	(numerator / v.len() as f64).sqrt()
}

pub fn simple_moving_average<T: Num + Convertible + Copy>(period: usize, v_data: &Vec<T>) -> Vec<f64> {
	let mut moving_average: Vec<f64> = vec![];
	let mut i: usize = 0;
	while i+period-1 < v_data.len() {
		let temp_vec: Vec<T> = v_data[i..i+period-1].to_vec();
		moving_average.push(mean(&temp_vec));
		i=i+1;
	}
	moving_average
}

pub fn get_bollinger_bands<T: Num + Convertible + Copy>(period: usize, n: f64, v_data: &Vec<T>) -> BollingerBands<f64> {
	let mut high: Vec<f64> = vec![];
	let mid: Vec<f64> = simple_moving_average(period, &v_data);
	let mut low: Vec<f64> = vec![];
	let mut i: usize = 0;
	while i+period-1 < v_data.len() {
		let temp_vec: Vec<T> = v_data[i..i+period-1].to_vec();
		let s_dev: f64 = std_dev(&temp_vec);
		high.push(mid[i] + s_dev*n);
		low.push(mid[i] - s_dev*n);
		i = i+1;
	}
	let b_bands = BollingerBands{
		high_band: high,
		mid_band: mid,
		low_band: low,
	};
	b_bands
}

