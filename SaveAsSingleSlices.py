# ----------------------------------------------------------------------------
# 
#  \file    SaveAsSingleSlices.py
#  \author  Birgit
#  \date    2017-04-13
#
#  save original, transformed and noisy slices from an image
# ----------------------------------------------------------------------------

from mevis import *
import os
import math


def export_function():
  
  path_patient = ctx.field("file_path_patient").value
  path_mask = ctx.field("file_path_mask").value
  filename_patient = ctx.field("filename_patient").value
  filename_mask = ctx.field("filename_mask").value
  
  check_input_image, check_paths, check_slice_numb, check_transf_numb, \
  check_noise_numb = check_input(path_patient, path_mask)
  
  # check if the paths exist and if the input parameters are okay
  if check_input_image == False:
    print("No CT and mask inputs")
  elif check_paths == False:  
    print("Invalid path")   
  elif check_slice_numb == False:    
    print("Invalid slice numbers")
  elif check_transf_numb == False:
    print("Invalid transformation parameters")
  elif check_noise_numb == False:
    print("Invalid noise parameters")
  else:
    set_datatype()
    
    # export original slices
    if ctx.field("original_bool").value == True:
      save_slices_patient(path_patient, filename_patient, "A")
      save_slices_mask(path_mask, filename_mask, "A")
      print("Original images are exported")
      
    # export transformed slices, distinguish between separate and combined
    if ctx.field("transform_bool").value == True:
      if ctx.field("combine_transform").value == False:
        separate_transformation(filename_patient, filename_mask, path_patient, path_mask)     
      else:      
        combined_transformation(filename_patient, filename_mask, path_patient, path_mask)
        
    # export noisy slices
    if ctx.field("noise_bool").value == True:
      noisy_slices(filename_patient, filename_mask, path_patient, path_mask)
      


#-----------------------------------------------------------------------------------------
# set data format
def set_datatype():
  ctx.field("SavePatient.format").value = ctx.field("data_type").value
  ctx.field("SaveMask.format").value = ctx.field("data_type").value
  ctx.field("SavePatientNoise.format").value = ctx.field("data_type").value
  ctx.field("SaveMaskNoise.format").value = ctx.field("data_type").value      



#-----------------------------------------------------------------------------------------
# Check Input
def check_input(path_patient, path_mask):
  check_input_image = True
  check_paths = True
  check_slice_numb = True
  check_transf_numb = True
  check_noise_numb = True
  
  if ctx.field("InfoPatient.sizeZ").value == 0 and \
    ctx.field("InfoMask.sizeZ").value != 0:
    print("No image input")
    
  if ctx.field("InfoMask.sizeZ").value == 0 and \
    ctx.field("InfoPatient.sizeZ").value != 0:
    print("No mask input")
    
  if ctx.field("InfoPatient.sizeZ").value == 0 and \
    ctx.field("InfoMask.sizeZ").value == 0:
    check_input_image = False

  if os.path.exists(path_patient) == False and os.path.isdir(path_patient) == False or\
    os.path.exists(path_mask) == False and os.path.isdir(path_mask) == False:  
    check_paths = False 
  
  if ctx.field("InfoPatient.sizeZ").value != 0:
    if ctx.field("first_slice").value > ctx.field("last_slice").value or \
      ctx.field("first_slice").value < 0 or ctx.field("last_slice").value < 0 or \
      ctx.field("first_slice").value >= ctx.field("InfoPatient.sizeZ").value or \
      ctx.field("last_slice").value >= ctx.field("InfoPatient.sizeZ").value:
      check_slice_numb = False
      
  if ctx.field("InfoPatient.sizeZ").value == 0 and \
    ctx.field("InfoMask.sizeZ").value != 0:
    if ctx.field("first_slice").value > ctx.field("last_slice").value or \
      ctx.field("first_slice").value < 0 or ctx.field("last_slice").value < 0 or \
      ctx.field("first_slice").value >= ctx.field("InfoMask.sizeZ").value or \
      ctx.field("last_slice").value >= ctx.field("InfoMask.sizeZ").value:
      check_slice_numb = False  
    
  if ctx.field("start_rotation").value > ctx.field("stop_rotation").value or \
    ctx.field("stepsize_rot").value <= 0 or \
    ctx.field("start_scalex").value > ctx.field("stop_scalex").value or \
    ctx.field("start_scaley").value > ctx.field("stop_scaley").value or\
    ctx.field("stepsize_scale").value <= 0:
    check_transf_numb = False
    
  if ctx.field("stepsize_uniform").value <= 0 or \
    ctx.field("amplitude_uniform_start").value > ctx.field("amplitude_uniform_stop").value or \
    ctx.field("stepsize_gauss").value <= 0 or \
    ctx.field("gauss_sigma_start").value > ctx.field("gauss_sigma_stop").value or \
    ctx.field("stepsize_sap").value <= 0 or \
    ctx.field("density_sap_start").value > ctx.field("density_sap_stop").value:
    check_noise_numb = False

  return check_input_image, check_paths, check_slice_numb, check_transf_numb, check_noise_numb

          
#-----------------------------------------------------------------------------------------
# Separate transformations
def separate_transformation(filename_patient, filename_mask, path_patient, path_mask):
  # Flip image
  if ctx.field("flip_bool").value == True:
    ctx.field("TransPatient.scalingX").value = -1
    ctx.field("TransMask.scalingX").value = -1
    new_filename_patient = filename_patient + "_Flip"
    new_filename_mask = filename_mask + "_Flip"
    save_slices_patient(path_patient, new_filename_patient, "A")
    save_slices_mask(path_mask, new_filename_mask, "A")
    print("Applied Transformation: Flipping")
    initial_transform_parameters()
      
  # Rotate image
  if ctx.field("rotate_bool").value == True:    
    start_rotation = ctx.field("start_rotation").value
    stop_rotation = ctx.field("stop_rotation").value + 1
    stepsize_rot = ctx.field("stepsize_rot").value
      
    for counter_rot in range(start_rotation, stop_rotation, stepsize_rot):
      if counter_rot == 0:
        pass
      else:
        # Set transformation parameters
        ctx.field("TransPatient.rotation").value = (counter_rot * math.pi)/180
        ctx.field("TransMask.rotation").value = (counter_rot * math.pi)/180
        new_filename_patient = filename_patient + "_Rot" + str(counter_rot)
        new_filename_mask = filename_mask + "_Rot" + str(counter_rot)
        save_slices_patient(path_patient, new_filename_patient, "A")
        save_slices_mask(path_mask, new_filename_mask, "A")         
    print("Applied Transformation: Rotation")
    initial_transform_parameters()
      
  # Scale Image
  if ctx.field("scale_bool").value == True:
    stepsize_scale = int(round(ctx.field("stepsize_scale").value * 100))
    start_scalex = int(round(ctx.field("start_scalex").value * 100))
    stop_scalex = int(round(ctx.field("stop_scalex").value * 100 + 1))
    start_scaley = int(round(ctx.field("start_scaley").value * 100))
    stop_scaley = int(round(ctx.field("stop_scaley").value * 100 + 1))     

    for counter_scalex in range(start_scalex, stop_scalex, stepsize_scale):
      counter_scalex_f = float(counter_scalex)/float(100)
      ctx.field("TransPatient.scalingX").value = counter_scalex_f
      ctx.field("TransMask.scalingX").value = counter_scalex_f
           
      # one loop for symmetric scaling
      if ctx.field("symmetric_scaling_bool").value == True:
        if counter_scalex == 100:
          pass
        else:
          ctx.field("TransPatient.scalingY").value = counter_scalex_f
          ctx.field("TransMask.scalingY").value = counter_scalex_f    
          new_filename_patient = filename_patient + "_X" + str(counter_scalex_f) + \
          "Y" + str(counter_scalex_f)
          new_filename_mask = filename_mask + "_X" + str(counter_scalex_f) + "Y" + \
          str(counter_scalex_f)
          save_slices_patient(path_patient, new_filename_patient, "A")
          save_slices_mask(path_mask, new_filename_mask, "A")
                
      else:
        # another loop for any scaling
        for counter_scaley in range(start_scaley, stop_scaley, stepsize_scale):
          if counter_scalex == 100 and counter_scaley == 100:
            pass
          else:    
            counter_scaley_f = float(counter_scaley)/float(100)
            ctx.field("TransPatient.scalingY").value = counter_scaley_f
            ctx.field("TransMask.scalingY").value = counter_scaley_f
            new_filename_patient = filename_patient + "_X" + str(counter_scalex_f) + \
            "Y" + str(counter_scaley_f)
            new_filename_mask = filename_mask + "_X" + str(counter_scalex_f) + "Y" + \
            str(counter_scaley_f)
            save_slices_patient(path_patient, new_filename_patient, "A")
            save_slices_mask(path_mask, new_filename_mask, "A")
          
    print("Applied Transformation: Scaling")
    initial_transform_parameters()      



#-----------------------------------------------------------------------------------------
# Combined transformation
def combined_transformation(filename_patient, filename_mask, path_patient, path_mask):
          
  flip_bool = ctx.field("flip_bool").value
  rotate_bool = ctx.field("rotate_bool").value
  scale_bool = ctx.field("scale_bool").value
  
  start_rotation = ctx.field("start_rotation").value
  stop_rotation = ctx.field("stop_rotation").value + 1
  stepsize_rot = ctx.field("stepsize_rot").value
  
  start_scalex = int(round(ctx.field("start_scalex").value * 100))
  stop_scalex = int(round(ctx.field("stop_scalex").value * 100 + 1))
  start_scaley = int(round(ctx.field("start_scaley").value * 100))
  stop_scaley = int(round(ctx.field("stop_scaley").value * 100 + 1))
  stepsize_scale = int(round(ctx.field("stepsize_scale").value * 100))
      
  # Flipping and Rotation
  if flip_bool == True and rotate_bool == True and scale_bool == False:
    ctx.field("TransPatient.scalingX").value = -1
    ctx.field("TransMask.scalingX").value = -1
          
    for counter_rot in range(start_rotation, stop_rotation, stepsize_rot):
      ctx.field("TransPatient.rotation").value = (counter_rot * math.pi)/180
      ctx.field("TransMask.rotation").value = (counter_rot * math.pi)/180
      new_filename_patient = filename_patient + "_Flip" + "Rot" + str(counter_rot)
      new_filename_mask = filename_mask + "_Flip" + "Rot" + str(counter_rot)
      save_slices_patient(path_patient, new_filename_patient, "A")
      save_slices_mask(path_mask, new_filename_mask, "A")     
          
    print("Applied Transformation: Flipping and Rotation")
    initial_transform_parameters()
          
  # Flipping and Scaling 
  elif flip_bool == True and scale_bool == True and rotate_bool == False:

    for counter_scalex in range(start_scalex, stop_scalex, stepsize_scale):
      counter_scalex_f = float(counter_scalex)/float(100)
      ctx.field("TransPatient.scalingX").value = -counter_scalex_f
      ctx.field("TransMask.scalingX").value = -counter_scalex_f
           
      # one loop for symmetric scaling
      if ctx.field("symmetric_scaling_bool").value == True:
        ctx.field("TransPatient.scalingY").value = counter_scalex_f
        ctx.field("TransMask.scalingY").value = counter_scalex_f    
        new_filename_patient = filename_patient + "_Flip" + "X" + str(counter_scalex_f) + \
        "Y" + str(counter_scalex_f)
        new_filename_mask = filename_mask + "_Flip" + "X" + str(counter_scalex_f) + "Y" + \
        str(counter_scalex_f)
        save_slices_patient(path_patient, new_filename_patient, "A")
        save_slices_mask(path_mask, new_filename_mask, "A")
                
      else:
        # another loop for any scaling
        for counter_scaley in range(start_scaley, stop_scaley, stepsize_scale):   
          counter_scaley_f = float(counter_scaley)/float(100)
          ctx.field("TransPatient.scalingY").value = counter_scaley_f
          ctx.field("TransMask.scalingY").value = counter_scaley_f
          new_filename_patient = filename_patient + "_Flip" + "X" + str(counter_scalex_f) + \
          "Y" + str(counter_scaley_f)
          new_filename_mask = filename_mask + "_Flip" + "X" + str(counter_scalex_f) + \
          "Y" + str(counter_scaley_f)
          save_slices_patient(path_patient, new_filename_patient, "A")
          save_slices_mask(path_mask, new_filename_mask, "A")
          
    print("Applied Transformation: Flipping and Scaling")
    initial_transform_parameters()
          
  # Rotation and Scaling
  elif rotate_bool == True and scale_bool == True and flip_bool == False:
          
    for counter_rot in range(start_rotation, stop_rotation, stepsize_rot):
      ctx.field("TransPatient.rotation").value = (counter_rot * math.pi)/180
      ctx.field("TransMask.rotation").value = (counter_rot * math.pi)/180

      for counter_scalex in range(start_scalex, stop_scalex, stepsize_scale):
        counter_scalex_f = float(counter_scalex)/float(100)
        ctx.field("TransPatient.scalingX").value = counter_scalex_f
        ctx.field("TransMask.scalingX").value = counter_scalex_f
           
        # one loop for symmetric scaling
        if ctx.field("symmetric_scaling_bool").value == True:
          ctx.field("TransPatient.scalingY").value = counter_scalex_f
          ctx.field("TransMask.scalingY").value = counter_scalex_f    
          new_filename_patient = filename_patient + "_Rot" + str(counter_rot) + \
          "X" + str(counter_scalex_f) + "Y" + str(counter_scalex_f)
          new_filename_mask = filename_mask + "_Rot" + str(counter_rot) + \
          "X" + str(counter_scalex_f) + "Y" + str(counter_scalex_f)
          save_slices_patient(path_patient, new_filename_patient, "A")
          save_slices_mask(path_mask, new_filename_mask, "A")
                
        else:
          # another loop for any scaling
          for counter_scaley in range(start_scaley, stop_scaley, stepsize_scale):   
            counter_scaley_f = float(counter_scaley)/float(100)
            ctx.field("TransPatient.scalingY").value = counter_scaley_f
            ctx.field("TransMask.scalingY").value = counter_scaley_f
            new_filename_patient = filename_patient + "_Rot" + str(counter_rot) + \
            "X" + str(counter_scalex_f) + "Y" + str(counter_scaley_f)
            new_filename_mask = filename_mask + "_Rot" + str(counter_rot) + \
            "X" + str(counter_scalex_f) + "Y" + str(counter_scaley_f)
            save_slices_patient(path_patient, new_filename_patient, "A")
            save_slices_mask(path_mask, new_filename_mask, "A")
          
    print("Applied Transformation: Rotation and Scaling")
    initial_transform_parameters()
          
  # Flipping, Scaling and Rotation
  elif rotate_bool == True and scale_bool == True and flip_bool == True:  
          
    for counter_rot in range(start_rotation, stop_rotation, stepsize_rot):
      ctx.field("TransPatient.rotation").value = (counter_rot * math.pi)/180
      ctx.field("TransMask.rotation").value = (counter_rot * math.pi)/180

      for counter_scalex in range(start_scalex, stop_scalex, stepsize_scale):
        counter_scalex_f = float(counter_scalex)/float(100)
        ctx.field("TransPatient.scalingX").value = -counter_scalex_f
        ctx.field("TransMask.scalingX").value = -counter_scalex_f
           
        # one loop for symmetric scaling
        if ctx.field("symmetric_scaling_bool").value == True:
          ctx.field("TransPatient.scalingY").value = counter_scalex_f
          ctx.field("TransMask.scalingY").value = counter_scalex_f    
          new_filename_patient = filename_patient + "_Flip" + "Rot" + str(counter_rot) + \
          "X" + str(counter_scalex_f) + "Y" + str(counter_scalex_f)
          new_filename_mask = filename_mask + "_Flip" + "Rot" + str(counter_rot) + \
          "X" + str(counter_scalex_f) + "Y" + str(counter_scalex_f)
          save_slices_patient(path_patient, new_filename_patient, "A")
          save_slices_mask(path_mask, new_filename_mask, "A")
                
        else:
          # another loop for any scaling
          for counter_scaley in range(start_scaley, stop_scaley, stepsize_scale):   
            counter_scaley_f = float(counter_scaley)/float(100)
            ctx.field("TransPatient.scalingY").value = counter_scaley_f
            ctx.field("TransMask.scalingY").value = counter_scaley_f
            new_filename_patient = filename_patient + "_Flip" + "Rot" + str(counter_rot) + \
            "X" + str(counter_scalex_f) + "Y" + str(counter_scaley_f)
            new_filename_mask = filename_mask + "_Flip" + "Rot" + str(counter_rot) + "X" + \
            str(counter_scalex_f) + "Y" + str(counter_scaley_f)
            save_slices_patient(path_patient, new_filename_patient, "A")
            save_slices_mask(path_mask, new_filename_mask, "A")
          
    print("Applied Transformation: Flipping, Rotation and Scaling")
    initial_transform_parameters()
  else:
    print("Too few transformation types are selceted")
    


#-----------------------------------------------------------------------------------------
# saves noisy slices
def noisy_slices(filename_patient, filename_mask, path_patient, path_mask):
  
  # uniform noise
  if ctx.field("type_uniform").value == True:
    ctx.field("AddNoisePatient.noiseType").value = "Uniform"
    ctx.field("AddNoiseMask.noiseType").value = "Uniform"
    ampl_uniform1 = ctx.field("amplitude_uniform_start").value
    ampl_uniform2 = ctx.field("amplitude_uniform_stop").value + 1
    stepsize_uniform = ctx.field("stepsize_uniform").value
    
    for counter_uniform in range(ampl_uniform1, ampl_uniform2, stepsize_uniform):
      ctx.field("AddNoisePatient.amplitude").value = counter_uniform
      ctx.field("AddNoiseMask.amplitude").value = counter_uniform
      new_filename_patient = filename_patient + "_Uniform" + str(counter_uniform)
      new_filename_mask = filename_mask + "_Uniform" + str(counter_uniform)
      save_slices_patient(path_patient, new_filename_patient, "N")
      save_slices_mask(path_mask, new_filename_mask, "N")
    print("Applied Noise: Uniform")
  
  # Gaussian noise
  if ctx.field("type_gauss").value == True:
    ctx.field("AddNoisePatient.noiseType").value = "Gaussian"
    ctx.field("AddNoiseMask.noiseType").value = "Gaussian"
    mean_value = ctx.field("gauss_mean_value").value
    ctx.field("AddNoisePatient.mean").value = mean_value
    ctx.field("AddNoiseMask.mean").value = mean_value
    sigma_start = ctx.field("gauss_sigma_start").value
    sigma_stop = ctx.field("gauss_sigma_stop").value + 1
    stepsize_gauss = ctx.field("stepsize_gauss").value
    
    for counter_gauss in range(sigma_start, sigma_stop, stepsize_gauss):
      ctx.field("AddNoisePatient.sigma").value = counter_gauss
      ctx.field("AddNoiseMask.sigma").value = counter_gauss
      new_filename_patient = filename_patient + "_Gauss" + str(mean_value) + \
      "_" + str(counter_gauss)
      new_filename_mask = filename_mask + "_Gauss" + str(mean_value) + \
      "_" + str(counter_gauss)
      save_slices_patient(path_patient, new_filename_patient, "N")
      save_slices_mask(path_mask, new_filename_mask, "N")
    print("Applied Noise: Gauss")
        
  # Salt and Pepper noise
  if ctx.field("type_saltpepper").value == True:
    ctx.field("AddNoisePatient.noiseType").value = "SaltPepper"
    ctx.field("AddNoiseMask.noiseType").value = "SaltPepper"
    ampl_salt = ctx.field("amplitude_salt").value
    ampl_pepper = ctx.field("amplitude_pepper").value
    density_start = int(round(ctx.field("density_sap_start").value * 100))
    density_stop = int(round(ctx.field("density_sap_stop").value * 100 + 1))
    stepsize_sap = int(round(ctx.field("stepsize_sap").value * 100))
    ctx.field("AddNoisePatient.amplitude").value = ampl_salt
    ctx.field("AddNoiseMask.amplitude").value = ampl_salt
    ctx.field("AddNoisePatient.amplitude2").value = ampl_pepper
    ctx.field("AddNoiseMask.amplitude2").value = ampl_pepper
    
    for counter_sap in range(density_start, density_stop, stepsize_sap):
      counter_sap_f = float(counter_sap)/float(100)
      ctx.field("AddNoisePatient.density").value = counter_sap_f
      ctx.field("AddNoiseMask.density").value = counter_sap_f
      new_filename_patient = filename_patient + "_SAP" + str(ampl_salt) + "_" + \
      str(ampl_pepper)+ "_" + str(round(counter_sap_f, 2))
      new_filename_mask = filename_mask + "_SAP" + str(ampl_salt) + "_" + \
      str(ampl_pepper) + "_" + str(round(counter_sap_f, 2))
      save_slices_patient(path_patient, new_filename_patient, "N")
      save_slices_mask(path_mask, new_filename_mask, "N")
    print("Applied Noise: Salt and Pepper")    
    


#-----------------------------------------------------------------------------------------
# saves slices of the patient
def save_slices_patient(new_path, new_filename, type_adj):
  
  progress_part = 0
  progress_counter = 0
  progress_finished = 1
  bool_every_slice = ctx.field("every_slice").value
  
  # parameters for saving all slices
  if bool_every_slice == True:
    number_slices = ctx.field("InfoPatient.sizeZ").value
    stop_slice = number_slices
    start_slice = 0
  
  # parameters for saving some slices
  else:
    start_slice = ctx.field("first_slice").value
    stop_slice = ctx.field("last_slice").value + 1 # +1 for correct loop
    number_slices = stop_slice - start_slice
    
  # loop for saving each slice
  for counter_slices in range(start_slice, stop_slice, 1):
    
    if type_adj == "N":
      ctx.field("SavePatientNoise.filename").value = os.path.join(new_path, new_filename + \
      "_Slice" + str(counter_slices))
      ctx.field("SubImagePatient.z").value = counter_slices
      ctx.field("SavePatientNoise.startTaskSynchronous").touch()
    else:
      ctx.field("SavePatient.filename").value = os.path.join(new_path, new_filename + \
      "_Slice" + str(counter_slices))
      ctx.field("SubImagePatient.z").value = counter_slices
      ctx.field("SavePatient.startTaskSynchronous").touch()     
    progress_counter += 1
    progress_part = float(progress_counter) / float(number_slices)
    ctx.field("export_progress").value = progress_part*0.5
    
  ctx.field("export_progress").value = progress_finished*0.5



#-----------------------------------------------------------------------------------------
# saves slices of the mask
def save_slices_mask(new_path, new_filename, type_adj):
  progress_part = 0
  progress_counter = 0
  progress_finished = 1
  bool_every_slice = ctx.field("every_slice").value
  
  # parameters for saving all slices
  if bool_every_slice == True:
    number_slices = ctx.field("InfoMask.sizeZ").value
    stop_slice = number_slices
    start_slice = 0
  
  # parameters for saving some slices
  else:
    start_slice = ctx.field("first_slice").value
    stop_slice = ctx.field("last_slice").value + 1 # +1 for correct loop
    number_slices = stop_slice - start_slice
    
  # loop for saving each slice
  for counter_slices in range(start_slice, stop_slice, 1):
    if type_adj == "N":
      ctx.field("SaveMaskNoise.filename").value = os.path.join(new_path, new_filename + \
      "_Slice" + str(counter_slices))
      ctx.field("SubImageMask.z").value = counter_slices
      ctx.field("SaveMaskNoise.startTaskSynchronous").touch()
    else:      
      ctx.field("SaveMask.filename").value = os.path.join(new_path, new_filename + \
      "_Slice" + str(counter_slices))
      ctx.field("SubImageMask.z").value = counter_slices
      ctx.field("SaveMask.startTaskSynchronous").touch()
    progress_counter += 1
    progress_part = (float(progress_counter) / float(number_slices)) + 0.5
    ctx.field("export_progress").value = progress_part

  ctx.field("export_progress").value = progress_finished



#-----------------------------------------------------------------------------------------
# set inital transformation parameters
def initial_transform_parameters():
  ctx.field("TransPatient.scalingX").value = 1
  ctx.field("TransMask.scalingX").value = 1
  ctx.field("TransPatient.scalingY").value = 1
  ctx.field("TransMask.scalingY").value = 1
  ctx.field("TransPatient.rotation").value = 0
  ctx.field("TransMask.rotation").value = 0 


