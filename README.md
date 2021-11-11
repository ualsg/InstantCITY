


Training:

python test.py --name xxx --netG local --ngf 32 --resize_or_crop none $@



python train.py --name xxx --dataroot ./datasets/Prepped/xxx --no_instance --batchSize 2



python train.py --name Berlin --dataroot ./datasets/Prepped/Berlin --no_instance --batchSize 2
python train.py --name Chicago --dataroot ./datasets/Prepped/Chicago --no_instance --batchSize 2
python train.py --name Singapore --dataroot ./datasets/Prepped/Singapore --no_instance --batchSize 2
python train.py --name Tokyo --dataroot ./datasets/Prepped/Tokyo --no_instance --batchSize 2
python train.py --name Manhattan --dataroot ./datasets/Prepped/Manhattan --no_instance --batchSize 2


python train.py --name Frankfurt15 --dataroot ./datasets/Prepped/Frankfurt15 --no_instance --batchSize 2
python train.py --name Jakarta15 --dataroot ./datasets/Prepped/Jakarta15 --no_instance --batchSize 2
python train.py --name Lesotho15 --dataroot ./datasets/Prepped/Lesotho15 --no_instance --batchSize 2

python train.py --name Beirut --dataroot ./datasets/Prepped/Beirut --no_instance --batchSize 2

python train.py --name Beirut --dataroot ./datasets/Prepped/Beirut --no_instance --batchSize 2





python train.py --name NY16 --dataroot ./datasets/Prepped/NY16 --no_instance --batchSize 2 & wait; 
python train.py --name Rotterdam16 --dataroot ./datasets/Prepped/Rotterdam16 --no_instance --batchSize 2 & wait; 
python train.py --name Seattle16 --dataroot ./datasets/Prepped/Seattle16 --no_instance --batchSize 2 & wait; 
python train.py --name SG16 --dataroot ./datasets/Prepped/SG16 --no_instance --batchSize 2 & wait; 


python train.py --name Frankfurt16 --dataroot ./datasets/Prepped/Frankfurt16 --no_instance --batchSize 2 & wait; 
python train.py --name Beirut16 --dataroot ./datasets/Prepped/Beirut16 --no_instance --batchSize 2 & wait;

## Commands to generate images with the same stucture as the input

#need to test these two once training is done
python test.py --name Beirut16 --dataroot ./datasets/Test/Beirut/input/16 --no_instance & wait;
python test.py --name Frankfurt16 --dataroot ./datasets/Test/Frankfurt/input/16 --no_instance & wait; 


python test.py --name Beirut15 --dataroot ./datasets/Test/Beirut/input/15 --no_instance & wait; 
python test.py --name Frankfurt15 --dataroot ./datasets/Test/Frankfurt/input/15 --no_instance & wait; 


python test.py --name Jakarta15 --dataroot ./datasets/Test/Jakarta/input/15 --no_instance & wait; 
python test.py --name Jakarta16 --dataroot ./datasets/Test/Jakarta/input/16 --no_instance & wait; 

python test.py --name London15 --dataroot ./datasets/Test/London/input/15 --no_instance & wait; 
python test.py --name London16 --dataroot ./datasets/Test/London/input/16 --no_instance & wait; 

python test.py --name NY15 --dataroot ./datasets/Test/NY/input/15 --no_instance & wait; 
python test.py --name NY116 --dataroot ./datasets/Test/NY/input/16 --no_instance & wait; 

python test.py --name Rotterdam15 --dataroot ./datasets/Test/Rotterdam/input/15 --no_instance & wait; 
python test.py --name Rotterdam16 --dataroot ./datasets/Test/Rotterdam/input/16 --no_instance & wait; 

python test.py --name Seattle15 --dataroot ./datasets/Test/Seattle/input/15 --no_instance & wait; 
python test.py --name Seattle16 --dataroot ./datasets/Test/Seattle/input/16 --no_instance & wait; 

python test.py --name SG15 --dataroot ./datasets/Test/SG/input/15 --no_instance & wait; 
python test.py --name SG16 --dataroot ./datasets/Test/SG/input/16 --no_instance & wait; 