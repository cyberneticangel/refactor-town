pub fn passing_average(scores: &Vec<i32>, pass_mark: i32) -> Option<f64> {
    let mut total = 0;
    let mut count = 0;
    let mut i = 0;
    while i < scores.len() {
        if scores[i] >= pass_mark {
            total = total + scores[i];
            count = count + 1;
        }
        i = i + 1;
    }
    if count == 0 {
        return None;
    }
    return Some(total as f64 / count as f64);
}

pub fn initials(names: &Vec<String>) -> String {
    let mut result = String::new();
    for i in 0..names.len() {
        let name = names[i].clone();
        if name.len() > 0 {
            let first = name.chars().nth(0).unwrap();
            result.push(first.to_ascii_uppercase());
        }
    }
    return result;
}

pub fn longest_word(text: &String) -> Option<String> {
    let words: Vec<String> = text.split_whitespace().map(|w| w.to_string()).collect();
    if words.len() == 0 {
        return None;
    }
    let mut best = words[0].clone();
    for i in 1..words.len() {
        if words[i].len() > best.len() {
            best = words[i].clone();
        }
    }
    return Some(best);
}
