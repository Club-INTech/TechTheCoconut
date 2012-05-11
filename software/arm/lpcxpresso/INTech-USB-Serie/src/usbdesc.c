/*----------------------------------------------------------------------------
 *      U S B  -  K e r n e l
 *----------------------------------------------------------------------------
 * Name:    usbdesc.c
 * Purpose: USB Descriptors
 * Version: V1.20
 *----------------------------------------------------------------------------
 *      This software is supplied "AS IS" without any warranties, express,
 *      implied or statutory, including but not limited to the implied
 *      warranties of fitness for purpose, satisfactory quality and
 *      noninfringement. Keil extends you a royalty-free right to reproduce
 *      and distribute executable files created using this software for use
 *      on NXP Semiconductors LPC microcontroller devices only. Nothing else 
 *      gives you the right to use this software.
 *
 * Copyright (c) 2009 Keil - An ARM Company. All rights reserved.
 *----------------------------------------------------------------------------
 * History:
 *          V1.20 Changed string descriptor handling
 *          V1.00 Initial Version
 *---------------------------------------------------------------------------*/
#include "type.h"
#include "usb.h"
#include "cdc.h"
#include "usbcfg.h"
#include "usbdesc.h"

 
/* USB Standard Device Descriptor */
const uint8_t USB_DeviceDescriptor[] = {
  USB_DEVICE_DESC_SIZE,              /* bLength */
  USB_DEVICE_DESCRIPTOR_TYPE,        /* bDescriptorType */
  WBVAL(0x0110), /* 1.10 */           /* bcdUSB WBVAL(0x0200) 2.0 */
  USB_DEVICE_CLASS_MISCELLANEOUS,   /* bDeviceClass CDC*/
  0x02,                              /* bDeviceSubClass */
  0x01,                              /* bDeviceProtocol */
  USB_MAX_PACKET0,                   /* bMaxPacketSize0 */
  WBVAL(0xFFFD),                     /* idVendor */
  WBVAL(0x2002),                     /* idProduct */
  WBVAL(0x0100), /* 1.00 */          /* bcdDevice */
  0x01,                              /* iManufacturer */
  0x02,                              /* iProduct */
  0x03,                              /* iSerialNumber */
  0x01                               /* bNumConfigurations: one possible configuration*/
};

/* USB Configuration Descriptor */
/*   All Descriptors (Configuration, Interface, Endpoint, Class, Vendor */
const uint8_t USB_ConfigDescriptor[] = {
/* Configuration 1 */
		  USB_CONFIGUARTION_DESC_SIZE,       /* bLength */
		  USB_CONFIGURATION_DESCRIPTOR_TYPE, /* bDescriptorType */
		  WBVAL(                             /* wTotalLength */
		    1*USB_CONFIGUARTION_DESC_SIZE +
		    (
		    8                             +  /* IAD */
		    1*USB_INTERFACE_DESC_SIZE     +  /* communication interface */
		    0x0013                        +  /* CDC functions */
		    1*USB_ENDPOINT_DESC_SIZE      +  /* interrupt endpoint */
		    1*USB_INTERFACE_DESC_SIZE     +  /* data interface */
		    2*USB_ENDPOINT_DESC_SIZE        /* bulk endpoints */
		    ) * 5							// 5
		      ),
		  USB_IF_NUM,                        /* bNumInterfaces */
		  0x01,                              /* bConfigurationValue: 0x01 is used to select this configuration */
		  0x00,                              /* iConfiguration: no string to describe this configuration */
		  USB_CONFIG_BUS_POWERED /*|*/       /* bmAttributes */
		/*USB_CONFIG_REMOTE_WAKEUP*/,
		  USB_CONFIG_POWER_MA(100),          /* bMaxPower, device power consumption is 100 mA */

		  /************************ CDC 0 ***************************/
		  /* IAD */
		      0x08,                                   // bLength
		      0x0B,                                   // bDescriptorType = 11
		      USB_CDC_CIF_NUM0,                       // bFirstInterface
		      0x02,                                   // bInterfaceCount
		      CDC_COMMUNICATION_INTERFACE_CLASS,      // bFunctionClass (Communication Class)
		      CDC_ABSTRACT_CONTROL_MODEL,             // bFunctionSubClass (Abstract Control Model)
		      0x01,                                   // bFunctionProcotol (V.25ter, Common AT commands)
		      0x00,                                   // iInterface
		  /* Interface 0, Alternate Setting 0, Communication class interface descriptor */
		    USB_INTERFACE_DESC_SIZE,           /* bLength */
		    USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
		    USB_CDC_CIF_NUM0,                   /* bInterfaceNumber: Number of Interface */
		    0x00,                              /* bAlternateSetting: Alternate setting */
		    0x01,                              /* bNumEndpoints: One endpoint used */
		    CDC_COMMUNICATION_INTERFACE_CLASS, /* bInterfaceClass: Communication Interface Class */
		    CDC_ABSTRACT_CONTROL_MODEL,        /* bInterfaceSubClass: Abstract Control Model */
		    0x01,                              /* bInterfaceProtocol: V.25ter, Common AT commands */
		    0x00,                              /* iInterface: */
		  /*Header Functional Descriptor*/
		    0x05,                              /* bLength: Endpoint Descriptor size */
		    CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
		    CDC_HEADER,                        /* bDescriptorSubtype: Header Func Desc */
		    WBVAL(CDC_V1_10), /* 1.10 */       /* bcdCDC */
		  /*Call Management Functional Descriptor*/
		    0x05,                              /* bFunctionLength */
		    CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
		    CDC_CALL_MANAGEMENT,               /* bDescriptorSubtype: Call Management Func Desc */
		    0x01,                              /* bmCapabilities: device handles call management */
		    USB_CDC_DIF_NUM0,                  /* bDataInterface: CDC data IF ID */
		  /*Abstract Control Management Functional Descriptor*/
		    0x04,                              /* bFunctionLength */
		    CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
		    CDC_ABSTRACT_CONTROL_MANAGEMENT,   /* bDescriptorSubtype: Abstract Control Management desc */
		    0x02,                              /* bmCapabilities: SET_LINE_CODING, GET_LINE_CODING, SET_CONTROL_LINE_STATE supported */
		  /*Union Functional Descriptor*/
		    0x05,                              /* bFunctionLength */
		    CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
		    CDC_UNION,                         /* bDescriptorSubtype: Union func desc */
		    USB_CDC_CIF_NUM0,                   /* bMasterInterface: Communication class interface is master */
		    USB_CDC_DIF_NUM0,                   /* bSlaveInterface0: Data class interface is slave 0 */
		  /*Endpoint 1 Descriptor*/            /* event notification (optional) */
		    USB_ENDPOINT_DESC_SIZE,            /* bLength */
		    USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
		    USB_ENDPOINT_IN(1),                /* bEndpointAddress */
		    USB_ENDPOINT_TYPE_INTERRUPT,       /* bmAttributes */
		    WBVAL(0x0010),                     /* wMaxPacketSize */
		    0x02,          /* 2ms */           /* bInterval */
		  /* Interface 1, Alternate Setting 0, Data class interface descriptor*/
		    USB_INTERFACE_DESC_SIZE,           /* bLength */
		    USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
		    USB_CDC_DIF_NUM0,                   /* bInterfaceNumber: Number of Interface */
		    0x00,                              /* bAlternateSetting: no alternate setting */
		    0x02,                              /* bNumEndpoints: two endpoints used */
		    CDC_DATA_INTERFACE_CLASS,          /* bInterfaceClass: Data Interface Class */
		    0x00,                              /* bInterfaceSubClass: no subclass available */
		    0x00,                              /* bInterfaceProtocol: no protocol used */
		    0x00,                              /* iInterface: */
		  /* Endpoint, EP2 Bulk Out */
		    USB_ENDPOINT_DESC_SIZE,            /* bLength */
		    USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
		    USB_ENDPOINT_OUT(2),               /* bEndpointAddress */
		    USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
		    WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
		    0x00,                              /* bInterval: ignore for Bulk transfer */
		  /* Endpoint, EP2 Bulk In */
		    USB_ENDPOINT_DESC_SIZE,            /* bLength */
		    USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
		    USB_ENDPOINT_IN(2),                /* bEndpointAddress */
		    USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
		    WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
		    0x00,                              /* bInterval: ignore for Bulk transfer */

		    /************************ CDC 1 ***************************/
		    /* IAD */
		        0x08,                                   // bLength
		        0x0B,                                   // bDescriptorType = 11
		        USB_CDC_CIF_NUM1,                       // bFirstInterface
		        0x02,                                   // bInterfaceCount
		        CDC_COMMUNICATION_INTERFACE_CLASS,      // bFunctionClass (Communication Class)
		        CDC_ABSTRACT_CONTROL_MODEL,             // bFunctionSubClass (Abstract Control Model)
		        0x01,                                   // bFunctionProcotol (V.25ter, Common AT commands)
		        0x00,                                   // iInterface
		    /* Interface 0, Alternate Setting 0, Communication class interface descriptor */
		      USB_INTERFACE_DESC_SIZE,           /* bLength */
		      USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
		      USB_CDC_CIF_NUM1,                   /* bInterfaceNumber: Number of Interface */
		      0x00,                              /* bAlternateSetting: Alternate setting */
		      0x01,                              /* bNumEndpoints: One endpoint used */
		      CDC_COMMUNICATION_INTERFACE_CLASS, /* bInterfaceClass: Communication Interface Class */
		      CDC_ABSTRACT_CONTROL_MODEL,        /* bInterfaceSubClass: Abstract Control Model */
		      0x01,                              /* bInterfaceProtocol: V.25ter, Common AT commands */
		      0x00,                              /* iInterface: */
		    /*Header Functional Descriptor*/
		      0x05,                              /* bLength: Endpoint Descriptor size */
		      CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
		      CDC_HEADER,                        /* bDescriptorSubtype: Header Func Desc */
		      WBVAL(CDC_V1_10), /* 1.10 */       /* bcdCDC */
		    /*Call Management Functional Descriptor*/
		      0x05,                              /* bFunctionLength */
		      CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
		      CDC_CALL_MANAGEMENT,               /* bDescriptorSubtype: Call Management Func Desc */
		      0x01,                              /* bmCapabilities: device handles call management */
		      USB_CDC_DIF_NUM1,                  /* bDataInterface: CDC data IF ID */
		    /*Abstract Control Management Functional Descriptor*/
		      0x04,                              /* bFunctionLength */
		      CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
		      CDC_ABSTRACT_CONTROL_MANAGEMENT,   /* bDescriptorSubtype: Abstract Control Management desc */
		      0x02,                              /* bmCapabilities: SET_LINE_CODING, GET_LINE_CODING, SET_CONTROL_LINE_STATE supported */
		    /*Union Functional Descriptor*/
		      0x05,                              /* bFunctionLength */
		      CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
		      CDC_UNION,                         /* bDescriptorSubtype: Union func desc */
		      USB_CDC_CIF_NUM1,                   /* bMasterInterface: Communication class interface is master */
		      USB_CDC_DIF_NUM1,                   /* bSlaveInterface0: Data class interface is slave 0 */
		    /*Endpoint 1 Descriptor*/            /* event notification (optional) */
		      USB_ENDPOINT_DESC_SIZE,            /* bLength */
		      USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
		      USB_ENDPOINT_IN(4),                /* bEndpointAddress */
		      USB_ENDPOINT_TYPE_INTERRUPT,       /* bmAttributes */
		      WBVAL(0x0010),                     /* wMaxPacketSize */
		      0x02,          /* 2ms */           /* bInterval */
		    /* Interface 1, Alternate Setting 0, Data class interface descriptor*/
		      USB_INTERFACE_DESC_SIZE,           /* bLength */
		      USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
		      USB_CDC_DIF_NUM1,                   /* bInterfaceNumber: Number of Interface */
		      0x00,                              /* bAlternateSetting: no alternate setting */
		      0x02,                              /* bNumEndpoints: two endpoints used */
		      CDC_DATA_INTERFACE_CLASS,          /* bInterfaceClass: Data Interface Class */
		      0x00,                              /* bInterfaceSubClass: no subclass available */
		      0x00,                              /* bInterfaceProtocol: no protocol used */
		      0x00,                              /* iInterface: */
		    /* Endpoint, EP2 Bulk Out */
		      USB_ENDPOINT_DESC_SIZE,            /* bLength */
		      USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
		      USB_ENDPOINT_OUT(5),               /* bEndpointAddress */
		      USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
		      WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
		      0x00,                              /* bInterval: ignore for Bulk transfer */
		    /* Endpoint, EP2 Bulk In */
		      USB_ENDPOINT_DESC_SIZE,            /* bLength */
		      USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
		      USB_ENDPOINT_IN(5),                /* bEndpointAddress */
		      USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
		      WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
		      0x00,                              /* bInterval: ignore for Bulk transfer */

		    //
		    // cut off CDC 2 - 4, to make this post short.
		    // To recover them,
		    // - Copy entire "CDC 0" descriptors
		    // - Replace all USB_CDC_CIF_NUM0, USB_CDC_DIF_NUM0 on CDC 0 to the corresponding ones
		    // - Replace three Endpoint numbers on the endpoint descriptors, interrupt IN, bulk IN/OUT
		    //
		    /************************ CDC 2 ***************************/
			  /* IAD */
				  0x08,                                   // bLength
				  0x0B,                                   // bDescriptorType = 11
				  USB_CDC_CIF_NUM2,                       // bFirstInterface
				  0x02,                                   // bInterfaceCount
				  CDC_COMMUNICATION_INTERFACE_CLASS,      // bFunctionClass (Communication Class)
				  CDC_ABSTRACT_CONTROL_MODEL,             // bFunctionSubClass (Abstract Control Model)
				  0x01,                                   // bFunctionProcotol (V.25ter, Common AT commands)
				  0x00,                                   // iInterface
			  /* Interface 0, Alternate Setting 0, Communication class interface descriptor */
				USB_INTERFACE_DESC_SIZE,           /* bLength */
				USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
				USB_CDC_CIF_NUM2,                   /* bInterfaceNumber: Number of Interface */
				0x00,                              /* bAlternateSetting: Alternate setting */
				0x01,                              /* bNumEndpoints: One endpoint used */
				CDC_COMMUNICATION_INTERFACE_CLASS, /* bInterfaceClass: Communication Interface Class */
				CDC_ABSTRACT_CONTROL_MODEL,        /* bInterfaceSubClass: Abstract Control Model */
				0x01,                              /* bInterfaceProtocol: V.25ter, Common AT commands */
				0x00,                              /* iInterface: */
			  /*Header Functional Descriptor*/
				0x05,                              /* bLength: Endpoint Descriptor size */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_HEADER,                        /* bDescriptorSubtype: Header Func Desc */
				WBVAL(CDC_V1_10), /* 1.10 */       /* bcdCDC */
			  /*Call Management Functional Descriptor*/
				0x05,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_CALL_MANAGEMENT,               /* bDescriptorSubtype: Call Management Func Desc */
				0x01,                              /* bmCapabilities: device handles call management */
				USB_CDC_DIF_NUM2,                  /* bDataInterface: CDC data IF ID */
			  /*Abstract Control Management Functional Descriptor*/
				0x04,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_ABSTRACT_CONTROL_MANAGEMENT,   /* bDescriptorSubtype: Abstract Control Management desc */
				0x02,                              /* bmCapabilities: SET_LINE_CODING, GET_LINE_CODING, SET_CONTROL_LINE_STATE supported */
			  /*Union Functional Descriptor*/
				0x05,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_UNION,                         /* bDescriptorSubtype: Union func desc */
				USB_CDC_CIF_NUM2,                   /* bMasterInterface: Communication class interface is master */
				USB_CDC_DIF_NUM2,                   /* bSlaveInterface0: Data class interface is slave 0 */
			  /*Endpoint 1 Descriptor*/            /* event notification (optional) */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_IN(7),                /* bEndpointAddress */
				USB_ENDPOINT_TYPE_INTERRUPT,       /* bmAttributes */
				WBVAL(0x0010),                     /* wMaxPacketSize */
				0x02,          /* 2ms */           /* bInterval */
			  /* Interface 1, Alternate Setting 0, Data class interface descriptor*/
				USB_INTERFACE_DESC_SIZE,           /* bLength */
				USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
				USB_CDC_DIF_NUM2,                   /* bInterfaceNumber: Number of Interface */
				0x00,                              /* bAlternateSetting: no alternate setting */
				0x02,                              /* bNumEndpoints: two endpoints used */
				CDC_DATA_INTERFACE_CLASS,          /* bInterfaceClass: Data Interface Class */
				0x00,                              /* bInterfaceSubClass: no subclass available */
				0x00,                              /* bInterfaceProtocol: no protocol used */
				0x00,                              /* iInterface: */
			  /* Endpoint, EP2 Bulk Out */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_OUT(8),               /* bEndpointAddress */
				USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
				WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
				0x00,                              /* bInterval: ignore for Bulk transfer */
			  /* Endpoint, EP2 Bulk In */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_IN(8),                /* bEndpointAddress */
				USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
				WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
				0x00,                              /* bInterval: ignore for Bulk transfer */
		    /************************ CDC 3 ***************************/
			  /* IAD */
				  0x08,                                   // bLength
				  0x0B,                                   // bDescriptorType = 11
				  USB_CDC_CIF_NUM3,                       // bFirstInterface
				  0x02,                                   // bInterfaceCount
				  CDC_COMMUNICATION_INTERFACE_CLASS,      // bFunctionClass (Communication Class)
				  CDC_ABSTRACT_CONTROL_MODEL,             // bFunctionSubClass (Abstract Control Model)
				  0x01,                                   // bFunctionProcotol (V.25ter, Common AT commands)
				  0x00,                                   // iInterface
			  /* Interface 0, Alternate Setting 0, Communication class interface descriptor */
				USB_INTERFACE_DESC_SIZE,           /* bLength */
				USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
				USB_CDC_CIF_NUM3,                   /* bInterfaceNumber: Number of Interface */
				0x00,                              /* bAlternateSetting: Alternate setting */
				0x01,                              /* bNumEndpoints: One endpoint used */
				CDC_COMMUNICATION_INTERFACE_CLASS, /* bInterfaceClass: Communication Interface Class */
				CDC_ABSTRACT_CONTROL_MODEL,        /* bInterfaceSubClass: Abstract Control Model */
				0x01,                              /* bInterfaceProtocol: V.25ter, Common AT commands */
				0x00,                              /* iInterface: */
			  /*Header Functional Descriptor*/
				0x05,                              /* bLength: Endpoint Descriptor size */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_HEADER,                        /* bDescriptorSubtype: Header Func Desc */
				WBVAL(CDC_V1_10), /* 1.10 */       /* bcdCDC */
			  /*Call Management Functional Descriptor*/
				0x05,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_CALL_MANAGEMENT,               /* bDescriptorSubtype: Call Management Func Desc */
				0x01,                              /* bmCapabilities: device handles call management */
				USB_CDC_DIF_NUM3,                  /* bDataInterface: CDC data IF ID */
			  /*Abstract Control Management Functional Descriptor*/
				0x04,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_ABSTRACT_CONTROL_MANAGEMENT,   /* bDescriptorSubtype: Abstract Control Management desc */
				0x02,                              /* bmCapabilities: SET_LINE_CODING, GET_LINE_CODING, SET_CONTROL_LINE_STATE supported */
			  /*Union Functional Descriptor*/
				0x05,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_UNION,                         /* bDescriptorSubtype: Union func desc */
				USB_CDC_CIF_NUM3,                   /* bMasterInterface: Communication class interface is master */
				USB_CDC_DIF_NUM3,                   /* bSlaveInterface0: Data class interface is slave 0 */
			  /*Endpoint 1 Descriptor*/            /* event notification (optional) */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_IN(10),                /* bEndpointAddress */
				USB_ENDPOINT_TYPE_INTERRUPT,       /* bmAttributes */
				WBVAL(0x0010),                     /* wMaxPacketSize */
				0x02,          /* 2ms */           /* bInterval */
			  /* Interface 1, Alternate Setting 0, Data class interface descriptor*/
				USB_INTERFACE_DESC_SIZE,           /* bLength */
				USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
				USB_CDC_DIF_NUM3,                   /* bInterfaceNumber: Number of Interface */
				0x00,                              /* bAlternateSetting: no alternate setting */
				0x02,                              /* bNumEndpoints: two endpoints used */
				CDC_DATA_INTERFACE_CLASS,          /* bInterfaceClass: Data Interface Class */
				0x00,                              /* bInterfaceSubClass: no subclass available */
				0x00,                              /* bInterfaceProtocol: no protocol used */
				0x00,                              /* iInterface: */
			  /* Endpoint, EP2 Bulk Out */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_OUT(11),               /* bEndpointAddress */
				USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
				WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
				0x00,                              /* bInterval: ignore for Bulk transfer */
			  /* Endpoint, EP2 Bulk In */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_IN(11),                /* bEndpointAddress */
				USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
				WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
				0x00,                              /* bInterval: ignore for Bulk transfer */
		    /************************ CDC 4 ***************************/
			  /* IAD */
				  0x08,                                   // bLength
				  0x0B,                                   // bDescriptorType = 11
				  USB_CDC_CIF_NUM4,                       // bFirstInterface
				  0x02,                                   // bInterfaceCount
				  CDC_COMMUNICATION_INTERFACE_CLASS,      // bFunctionClass (Communication Class)
				  CDC_ABSTRACT_CONTROL_MODEL,             // bFunctionSubClass (Abstract Control Model)
				  0x01,                                   // bFunctionProcotol (V.25ter, Common AT commands)
				  0x00,                                   // iInterface
			  /* Interface 0, Alternate Setting 0, Communication class interface descriptor */
				USB_INTERFACE_DESC_SIZE,           /* bLength */
				USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
				USB_CDC_CIF_NUM4,                   /* bInterfaceNumber: Number of Interface */
				0x00,                              /* bAlternateSetting: Alternate setting */
				0x01,                              /* bNumEndpoints: One endpoint used */
				CDC_COMMUNICATION_INTERFACE_CLASS, /* bInterfaceClass: Communication Interface Class */
				CDC_ABSTRACT_CONTROL_MODEL,        /* bInterfaceSubClass: Abstract Control Model */
				0x01,                              /* bInterfaceProtocol: V.25ter, Common AT commands */
				0x00,                              /* iInterface: */
			  /*Header Functional Descriptor*/
				0x05,                              /* bLength: Endpoint Descriptor size */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_HEADER,                        /* bDescriptorSubtype: Header Func Desc */
				WBVAL(CDC_V1_10), /* 1.10 */       /* bcdCDC */
			  /*Call Management Functional Descriptor*/
				0x05,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_CALL_MANAGEMENT,               /* bDescriptorSubtype: Call Management Func Desc */
				0x01,                              /* bmCapabilities: device handles call management */
				USB_CDC_DIF_NUM4,                  /* bDataInterface: CDC data IF ID */
			  /*Abstract Control Management Functional Descriptor*/
				0x04,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_ABSTRACT_CONTROL_MANAGEMENT,   /* bDescriptorSubtype: Abstract Control Management desc */
				0x02,                              /* bmCapabilities: SET_LINE_CODING, GET_LINE_CODING, SET_CONTROL_LINE_STATE supported */
			  /*Union Functional Descriptor*/
				0x05,                              /* bFunctionLength */
				CDC_CS_INTERFACE,                  /* bDescriptorType: CS_INTERFACE */
				CDC_UNION,                         /* bDescriptorSubtype: Union func desc */
				USB_CDC_CIF_NUM4,                   /* bMasterInterface: Communication class interface is master */
				USB_CDC_DIF_NUM4,                   /* bSlaveInterface0: Data class interface is slave 0 */
			  /*Endpoint 1 Descriptor*/            /* event notification (optional) */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_IN(13),                /* bEndpointAddress */
				USB_ENDPOINT_TYPE_INTERRUPT,       /* bmAttributes */
				WBVAL(0x0010),                     /* wMaxPacketSize */
				0x02,          /* 2ms */           /* bInterval */
			  /* Interface 1, Alternate Setting 0, Data class interface descriptor*/
				USB_INTERFACE_DESC_SIZE,           /* bLength */
				USB_INTERFACE_DESCRIPTOR_TYPE,     /* bDescriptorType */
				USB_CDC_DIF_NUM4,                   /* bInterfaceNumber: Number of Interface */
				0x00,                              /* bAlternateSetting: no alternate setting */
				0x02,                              /* bNumEndpoints: two endpoints used */
				CDC_DATA_INTERFACE_CLASS,          /* bInterfaceClass: Data Interface Class */
				0x00,                              /* bInterfaceSubClass: no subclass available */
				0x00,                              /* bInterfaceProtocol: no protocol used */
				0x00,                              /* iInterface: */
			  /* Endpoint, EP2 Bulk Out */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_OUT(14),               /* bEndpointAddress */
				USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
				WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
				0x00,                              /* bInterval: ignore for Bulk transfer */
			  /* Endpoint, EP2 Bulk In */
				USB_ENDPOINT_DESC_SIZE,            /* bLength */
				USB_ENDPOINT_DESCRIPTOR_TYPE,      /* bDescriptorType */
				USB_ENDPOINT_IN(14),                /* bEndpointAddress */
				USB_ENDPOINT_TYPE_BULK,            /* bmAttributes */
				WBVAL(USB_CDC_BUFSIZE),            /* wMaxPacketSize */
				0x00,                              /* bInterval: ignore for Bulk transfer */

		    /* Terminator */
		      0                                  /* bLength */
};




/* USB String Descriptor (optional) */
const uint8_t USB_StringDescriptor[] = {
/* Index 0x00: LANGID Codes */
  0x04,                              /* bLength */
  USB_STRING_DESCRIPTOR_TYPE,        /* bDescriptorType */
  WBVAL(0x0409), /* US English */    /* wLANGID */
/* Index 0x01: Manufacturer */
  (13*2 + 2),                        /* bLength (13 Char + Type + lenght) */
  USB_STRING_DESCRIPTOR_TYPE,        /* bDescriptorType */
  'N',0,
  'X',0,
  'P',0,
  ' ',0,
  'S',0,
  'E',0,
  'M',0,
  'I',0,
  'C',0,
  'O',0,
  'N',0,
  'D',0,
  ' ',0,
/* Index 0x02: Product */
  (17*2 + 2),                        /* bLength ( 17 Char + Type + lenght) */
  USB_STRING_DESCRIPTOR_TYPE,        /* bDescriptorType */
  'N',0,
  'X',0,
  'P',0,
  ' ',0,
  'L',0,
  'P',0,
  'C',0,
  '1',0,
  '7',0,
  'x',0,
  'x',0,
  ' ',0,
  'V',0,
  'C',0,
  'O',0,
  'M',0,
  ' ',0,
/* Index 0x03: Serial Number */
  (12*2 + 2),                        /* bLength (12 Char + Type + lenght) */
  USB_STRING_DESCRIPTOR_TYPE,        /* bDescriptorType */
  'D',0,
  'E',0,
  'M',0,
  'O',0,
  '0',0,
  '0',0,
  '0',0,
  '0',0,
  '0',0,
  '0',0,
  '0',0,
  '0',0,
/* Index 0x04: Interface 0, Alternate Setting 0 */
  ( 4*2 + 2),                        /* bLength (4 Char + Type + lenght) */
  USB_STRING_DESCRIPTOR_TYPE,        /* bDescriptorType */
  'V',0,
  'C',0,
  'O',0,
  'M',0,
};
