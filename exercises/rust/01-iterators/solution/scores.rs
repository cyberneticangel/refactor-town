pub fn passing_average(scores: &[i32], pass_mark: i32) -> Option<f64> {
    let passing: Vec<i32> = scores.iter().copied().filter(|&s| s >= pass_mark).collect();
    if passing.is_empty() {
        return None;
    }
    let total: i32 = passing.iter().sum();
    Some(total as f64 / passing.len() as f64)
}

pub fn initials(names: &[String]) -> String {
    names
        .iter()
        .filter_map(|name| name.chars().next())
        .map(|c| c.to_ascii_uppercase())
        .collect()
}

pub fn longest_word(text: &str) -> Option<&str> {
    // max_by_key returns the *last* maximum, so reverse to keep the first one on ties
    text.split_whitespace().rev().max_by_key(|word| word.len())
}
