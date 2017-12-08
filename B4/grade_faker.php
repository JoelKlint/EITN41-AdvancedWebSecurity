<?php

function calc_signature($name, $grade) {
    $data = $name . $grade;
    echo substr(hash_hmac("sha1", $data, $key), 0, 20) . "\n";
}

calc_signature("Kalle", "5");