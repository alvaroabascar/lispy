(define fact
    (lambda (x)
        (if (<= x 1)
            x
            (* x (fact (- x 1))))))

(define fact-of-10 (fact 10))

(display fact-of-10)
