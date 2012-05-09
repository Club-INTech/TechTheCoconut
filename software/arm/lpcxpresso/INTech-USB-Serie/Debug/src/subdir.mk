################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/cdcuser.c \
../src/cr_startup_lpc176x.c \
../src/delay.c \
../src/gpio.c \
../src/serial.c \
../src/uart.c \
../src/usbcore.c \
../src/usbdesc.c \
../src/usbhw.c \
../src/usbuser.c \
../src/vcomdemo.c 

OBJS += \
./src/cdcuser.o \
./src/cr_startup_lpc176x.o \
./src/delay.o \
./src/gpio.o \
./src/serial.o \
./src/uart.o \
./src/usbcore.o \
./src/usbdesc.o \
./src/usbhw.o \
./src/usbuser.o \
./src/vcomdemo.o 

C_DEPS += \
./src/cdcuser.d \
./src/cr_startup_lpc176x.d \
./src/delay.d \
./src/gpio.d \
./src/serial.d \
./src/uart.d \
./src/usbcore.d \
./src/usbdesc.d \
./src/usbhw.d \
./src/usbuser.d \
./src/vcomdemo.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__USE_CMSIS=CMSISv2_LPC17xx -D__REDLIB__ -I"C:\Users\Nils\Documents\LPCXpresso_4.2.0_264\workspace\CMSISv2_LPC17xx" -I"C:\Users\Nils\Documents\LPCXpresso_4.2.0_264\workspace\CMSISv2_LPC17xx\inc" -O0 -Wall -c -fmessage-length=0 -fno-builtin -ffunction-sections -fdata-sections -mcpu=cortex-m3 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

src/cr_startup_lpc176x.o: ../src/cr_startup_lpc176x.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__USE_CMSIS=CMSISv2_LPC17xx -D__REDLIB__ -I"C:\Users\Nils\Documents\LPCXpresso_4.2.0_264\workspace\CMSISv2_LPC17xx" -I"C:\Users\Nils\Documents\LPCXpresso_4.2.0_264\workspace\CMSISv2_LPC17xx\inc" -O0 -Os -Wall -c -fmessage-length=0 -fno-builtin -ffunction-sections -fdata-sections -mcpu=cortex-m3 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"src/cr_startup_lpc176x.d" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


