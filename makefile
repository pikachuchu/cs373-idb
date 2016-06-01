FILES :=                                          \
    .gitignore                                    \
    makefile                                      \
    class_requirements/apiary.apib                \
    class_requirements/IDB1.log                   \
    class_requirements/IDB2.log                   \
    class_requirements/IDB3.log                   \
    politicianhub/models.py                       \
    class_requirements/model.html                 \
    tests.py                                      \
    class_requirements/UML.pdf

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__

coverage:
	coverage run --branch tests.py
	coverage report --include=politicianhub/models.py

test:
	python tests.py

populate:
	python politicianhub/models.py

mysql:
	mysql --host=173.194.239.21 --user=testing --password
